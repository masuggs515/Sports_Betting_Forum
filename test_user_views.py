"""User View tests."""

import os
from unittest import TestCase
from flask import g

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///sports_forum_test"

from app import app, CURR_USER_KEY

db.create_all()
app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):

    def setUp(self):
        """Create test user and data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser")
        self.testuser_id = 25
        self.testuser.id = self.testuser_id

        

        db.session.commit()
    
    def test_show_user(self):
        user = User.query.get_or_404(self.testuser_id)
        with self.client as client:
            res = client.get(f'/user/{user.id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<h4 class="mt-0 mb-0">{user.username}</h4>' , html)


    def test_user_edit(self):
        user = User.query.get_or_404(self.testuser_id)
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            res = client.get(f'/user/{user.id}/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f"<h2 class=\"mt-3 join-message text-center\">Edit {user.username}'s Profile</h2>", html)