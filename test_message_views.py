"""Message View tests."""

import os
from unittest import TestCase
from models import db, Message, User

# using test database for tests

os.environ['DATABASE_URL'] = "postgresql:///waddle-test"

from app import app, CURR_USER_KEY

# create tables once for all tests
# in each test we delete the data and create new clean test data

db.create_all()

# Don't have WTForms use CSRF

app.config['WTF_CSRF_ENABLED'] = False

class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def tearDown(self):
        """Clear sample data after each test."""

        User.query.delete()
        db.session.commit()
        Message.query.delete()
        db.session.commit()

    def test_add_message(self):
        """Testing if can add a message"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    def test_show_message(self):
        """Testing if can show a message"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/messages/new", data={"text": "Hello"})

            message_id = Message.query.filter(Message.user_id==self.testuser.id).one().id

            resp_show = c.get(f"/messages/{message_id}")

            self.assertEqual(resp_show.status_code, 200)
            self.assertIn(b"Hello", resp_show.data)

    def test_delete_message(self):
        """Testing if can delete a message"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/messages/new", data={"text": "Hello"})

            message_id = Message.query.filter(Message.user_id==self.testuser.id).one().id

            before_delete = Message.query.all()

            self.assertEqual(len(before_delete), 1)

            resp_del = c.post(f"/messages/{message_id}/delete")

            self.assertEqual(resp.status_code, 302)

            after_delete = Message.query.all()

            self.assertEqual(len(after_delete), 0)
