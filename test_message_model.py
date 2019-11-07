import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Follows, bcrypt
from datetime import datetime

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
from app import app
# Now we can import app
# from seed import seed_data
# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
    """Test for the Message model."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

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
        """Testing to see if message's user's id is correct."""

        test_query = Message.query.get_or_404(1)
        self.assertEqual(test_query.user_id, 1)
        self.assertNotEqual(test_query.user_id, 2)
