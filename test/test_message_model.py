"""Message model tests."""

import os
from unittest import TestCase
from models import db, User, Message, Follows
from datetime import datetime

# using test database for tests

os.environ['DATABASE_URL'] = "postgresql:///waddle-test"

from app import app

# create tables once for all tests
# in each test we delete the data and create new clean test data

db.create_all()

class MessageModelTestCase(TestCase):
    """Test for the Message model."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password='PASSWORD',
            image_url=None
        )
        u.id = 1
        db.session.add(u)
        db.session.commit()

        test_message = Message(id=1, text='i am whiskey',
                               user_id=u.id, timestamp=datetime.utcnow())
        db.session.add(test_message)
        db.session.commit()

    def tearDown(self):
        """Clear sample data after each test."""

        User.query.delete()
        db.session.commit()
        Message.query.delete()
        db.session.commit()
        Follows.query.delete()
        db.session.commit()

    def test_message_model(self):
        """Testing if basic message model works."""

        self.assertEqual(Message.query.count(), 1)

    def test_text(self):
        """Testing to see if message's text is correct."""
        test_query = Message.query.get_or_404(1)
        self.assertEqual(test_query.text, 'i am whiskey')
        self.assertNotEqual(test_query.text, 'i am whiskey food')
    
    def test_timestamp(self):
        """Testing to see if message's timestamp is correct."""

        test_query = Message.query.get_or_404(1)
        self.assertTrue(test_query.timestamp)

    def test_user_id(self):
        """Testing to see if if id for person who posted the
        message is correct."""

        test_query = Message.query.get_or_404(1)
        self.assertEqual(test_query.user_id, 1)
        self.assertNotEqual(test_query.user_id, 2)
