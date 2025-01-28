"""User view tests."""

import os
from unittest import TestCase
from models import db, User, Message, Follows
from datetime import datetime
from app import app, CURR_USER_KEY

# using test database for tests

os.environ['DATABASE_URL'] = "postgresql:///waddle-test"

# create tables once for all tests
# in each test we delete the data and create new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password='PASSWORD',
            image_url=None
        )

        db.session.add(u)
        db.session.commit()

        self.user = u

        u_two = User.signup(
            email="test2@test.com",
            username="testuserasDASKD",
            password='PASSWORD',
            image_url=None
        )
        u_two.id = 2
        db.session.add(u_two)
        db.session.commit()

        test_follow = Follows(user_being_followed_id=u.id,
                              user_following_id=u_two.id)
        db.session.add(test_follow)
        db.session.commit()

        test_follow_2 = Follows(user_being_followed_id=u_two.id,
                                user_following_id=u.id)
        db.session.add(test_follow_2)
        db.session.commit()

        test_message = Message(text='i am whiskey',
                               user_id=self.user.id, timestamp=datetime.utcnow())
        db.session.add(test_message)
        db.session.commit()

        self.message = test_message

    def tearDown(self):
        """Clear sample data after each test."""

        User.query.delete()
        db.session.commit()
        Message.query.delete()
        db.session.commit()
        Follows.query.delete()
        db.session.commit()

    def test_view_following(self):
        """Test to see if you can see following pages when logged in."""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            resp = client.get(f'users/{self.user.id}/following')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3 class="following-header">Following</h3>',
                          resp.data.decode('utf-8'))

    def test_logged_out_visiting(self):
        """Test to see if you are prevented from viewing a user's
        follower/following page if you are not logged in"""

        with app.test_client() as client:
            resp = client.get(
                f'users/{self.user.id}/following')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/")

    def test_adding_a_message(self):
        """Testing to see if logged in user can send a message as themselves"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            user = User.query.get_or_404(self.user.id)
            msg_len = len(user.messages)
            resp = client.post('/messages/new', 
                               data={'text': 'i am whiskey2', 
                                    'user_id': user.id, 
                                    'timestamp': datetime.utcnow()})

            self.assertEqual(resp.status_code, 302)
            w = Message.query.filter_by(text="i am whiskey2").first()
            self.assertIsNotNone(w)
            self.assertEqual(len(user.messages), msg_len + 1)

    def test_deleting_a_message(self):
        """Testing to see if logged in user can delete a message as themselves"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            user = User.query.get_or_404(self.user.id)
            msg = Message.query.get_or_404(user.messages[0].id)
            msg_len = len(user.messages)
            resp = client.post(f'messages/{msg.id}/delete')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(len(user.messages), msg_len - 1)

    def test_logged_out_create_msg(self):
        """Testing to see if can create message when logged out."""
        
        with app.test_client() as client:
            resp = client.post('/messages/new', 
                               data={'text': 'i am whiskey2', 
                                    'user_id': self.user.id, 
                                    'timestamp': datetime.utcnow()})
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/")
    
    def test_logged_out_delete_msg(self):
        """Testing to see if can delete message when logged out."""
        
        with app.test_client() as client:
            user = User.query.get_or_404(self.user.id)
            msg = Message.query.get_or_404(user.messages[0].id)
            resp = client.post(f'messages/{msg.id}/delete')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/")
    
    def test_create_msg_as_another(self):
        """Testing to see if you can create message as another user."""
        
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            q = User.query.get(2)
            q_len = len(q.messages)
            resp = client.post('/messages/new', 
                               data={'text': 'i am whiskey2', 
                                    'user_id': 2, 
                                    'timestamp': datetime.utcnow()})
            self.assertEqual(q_len, len(q.messages))
