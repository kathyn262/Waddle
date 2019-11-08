"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///waddle-test"

# Now we can import app
# from seed import seed_data
from app import app
# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

PASSWORD = "Passsword"


class UserModelTestCase(TestCase):
    """Tests for the User model."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()
        # seed_data()

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password=PASSWORD,
            image_url=None
        )
        u.id = 1
        db.session.add(u)
        db.session.commit()

        u_two = User.signup(
            email="test2@test.com",
            username="testuserasDASKD",
            password=PASSWORD,
            image_url=None
        )
        u_two.id = 2
        db.session.add(u_two)
        db.session.commit()

        test_follow = Follows(user_being_followed_id=u.id,
                              user_following_id=u_two.id)
        db.session.add(test_follow)
        db.session.commit()

    def tearDown(self):
        """Clear sample data after each test."""
        
        User.query.delete()
        db.session.commit()
        Message.query.delete()
        db.session.commit()
        Follows.query.delete()
        db.session.commit()

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        test_query_two = User.query.get_or_404(2)
        self.assertEqual(len(test_query_two.messages), 0)
        self.assertEqual(len(test_query_two.followers), 0)

    def test_repr(self):
        """Testing the repr method."""

        self.assertEqual(User.__repr__(User(id=1, username='testuser',
                                            email='test@test.com')), "<User #1: testuser, test@test.com>")

    def test_is_following(self):
        """Testing if user2 is following user1."""
        test_query_one = User.query.get_or_404(1)
        test_query_two = User.query.get_or_404(2)

        self.assertEqual(User.is_following(
            test_query_two, test_query_one), True)

    def test_if_not_following(self):
        """Testing if user1 is not following user2."""
        test_query_one = User.query.get_or_404(1)
        test_query_two = User.query.get_or_404(2)

        self.assertEqual(User.is_following(
            test_query_one, test_query_two), False)

    def test_is_followed_by(self):
        """Testing if user1 is followed by user2."""
        test_query_one = User.query.get_or_404(1)
        test_query_two = User.query.get_or_404(2)

        self.assertEqual(User.is_followed_by(
            test_query_one, test_query_two), True)

    def test_is_not_followed_by(self):
        """Testing if user2 is not followed by user1."""
        test_query_one = User.query.get_or_404(1)
        test_query_two = User.query.get_or_404(2)

        self.assertEqual(User.is_followed_by(
            test_query_two, test_query_one), False)

    def test_user_creation_method(self):
        """Testing if a created user is added to db"""
        user_count = User.query.count()
        new_user = User.signup(
            'uniquenewyork', 'unique@email.com', 'uniquepassword', '')
        db.session.add(new_user)
        db.session.commit()
        self.assertEqual(User.query.count(), user_count + 1)
        self.assertNotEqual(User.query.count(), user_count + 2)


    def test_user_creation_method_fail(self):
        """Making sure user with invalid credentials is not added"""
        new_user = User(
            username='testuser', email='unique@email.com', password='uniquepassword')
        self.assertEqual(
            new_user.id, None)

    def test_user_authenticate(self):
        """Testing that user's with valid credentials are authenticated successfully"""
        test_query_one = User.query.get_or_404(1)
        authentication = User.authenticate(test_query_one.username, PASSWORD)
        self.assertTrue(authentication)

    def test_user_authenticate_fail_username(self):
        """Testing that user's with an invalid username is not validated"""
        authentication = User.authenticate('badusername', PASSWORD)
        self.assertFalse(authentication)

    def test_user_authenticate_fail_password(self):
        """Testing that user's with an invalid password is not validated"""
        test_query_one = User.query.get_or_404(1)
        authentication = User.authenticate(
            test_query_one.username, 'BADPASSWORD')
        self.assertFalse(authentication)
