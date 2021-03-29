"""User model tests."""
import os
from unittest import TestCase

from models import db, User
from sqlalchemy import exc


os.environ['DATABASE_URL'] = "postgresql:///sports_forum_test"


from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1","password", "email1@email.com")
        user_id1 = 11
        u1.id = user_id1

        u2 = User.signup("test2", "password", "email2@email.com")
        user_id2 = 22
        u2.id = user_id2

        db.session.commit()

        u1 = User.query.get(user_id1)
        u2 = User.query.get(user_id2)

        self.u1 = u1
        self.uid1 = user_id1

        self.u2 = u2
        self.uid2 = user_id2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_user_model(self):
        """Does basic model work?"""
    
        u = User(
            id=44,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.like), 0)
        self.assertEqual(len(u.comment), 0)

    # Testing Signup section

    def test_signup(self):
        u_signup = User.signup("test_user", "test_password", "test_user@test.com")
        test_id = 1234
        u_signup.id = test_id
        db.session.commit()

        user_test = User.query.get_or_404(test_id)
        self.assertEqual(user_test.id, 1234)
        self.assertEqual(user_test.username, "test_user")
        self.assertNotEqual(user_test.password, "test_password")
        self.assertTrue(user_test.password.startswith("$2b$12"))

    def test_signup_invalid_username(self):
        u_signup = User.signup(None, "test_password", "test_user@test.com")
        test_id = 777
        u_signup.id = test_id

        with self.assertRaises(exc.IntegrityError) as test:
            db.session.commit()

    def test_signup_invalid_email(self):
        u_signup = User.signup("TestUser", "test_password", None)
        test_id = 777
        u_signup.id = test_id

        with self.assertRaises(exc.IntegrityError) as test:
            db.session.commit()

    def test_signup_invalid_password(self):
        with self.assertRaises(ValueError) as test:
            User.signup("testtest", "", "email@email.com")

    # Testing authentication

    def test_auth(self):
        test = User.authenticate(self.u2.username, 'password')
        self.assertIsNotNone(test)

    def test_username_fail(self):
        self.assertFalse(User.authenticate("testtesttest3", "password"))

    def test_incorrect_pwd(self):
        self.assertFalse(User.authenticate(self.u2.username, "password2"))