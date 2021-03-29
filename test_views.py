"""User View tests."""

import os
from unittest import TestCase
from flask import g

from models import db, User, Game, Like, Comment

os.environ['DATABASE_URL'] = "postgresql:///sports_forum_test"

from app import app, CURR_USER_KEY

db.create_all()
app.config['WTF_CSRF_ENABLED'] = False

class LeagueViewTestCase(TestCase):
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


        g1 = Game(team_one="TestTeam", team_two="TestTeam2", team_one_odds=1.0, team_two_odds= -1.0)
        game_id1 = 'id123'
        g1.id = game_id1

        db.session.add(g1)
        db.session.commit()

        c = Comment(user_id = self.testuser.id, game_id = game_id1, text="Test Text")
        c.id = 33
        db.session.add(c)
        db.session.commit()

        test_like = Like(user_id=self.testuser_id, comment_id=c.id)
        test_like.id = 254
        db.session.add(test_like)
        db.session.commit()
        
        self.like = Like.query.filter(Like.comment_id==33, Like.user_id==25).one()
        self.comment_1 = Comment.query.get(33)
        self.game_1 = Game.query.get(game_id1)
        self.game_1id = game_id1
        self.commentid = c.id

    def test_show_leagues(self):
        with self.client as client:
            res = client.get(f'/leagues')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<h2 class="text-light-grey text-center mt-3">All Leagues Available</h2>' , html)

    def test_show_game(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            res = client.get(f'/game/{self.game_1id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<div class="mx-2"><a class="text-light-grey text-decoration-none fw-bold" href="/user/{self.testuser.id}">{self.testuser.username}' , html)
            self.assertIn(f'TestTeam' , html)
            self.assertIn(f'<div id="{self.commentid}"' , html)
            self.assertIn(f'fas fa-thumbs-up' , html)
            self.assertIn(f'Test Text' , html)
            self.assertNotIn(f'No comments yet, Get the conversation started!' , html)


class LoginRegisterViewCase(TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

    def test_login_page(self):
        with self.client as client:
            res = client.get('/login')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="text-center display-2 my-3">Welcome to SportDiscuss</h1>', html)
            self.assertIn('<div class="mx-2"><a class="text-light-grey text-decoration-none fw-bold" href="/signup">Sign up / Login</a></div>', html)
            self.assertIn('<h2 class="join-message  pt-5 text-center text-light-grey ">Welcome Back</h2>', html)

    def test_signup_page(self):
        with self.client as client:
            res = client.get('/signup')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<a href="/signup" class="text-decoration-none text-center col-5 bg-green register-active pt-2 pb-1  text-dark-blue"', html)
            self.assertIn('<h2 class="join-message mx-4 pt-3 text-center text-light-grey">Join SportDiscuss', html)


    def test_404_page(self):
        with self.client as client:
            res = client.get('/signpu')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 404)
            self.assertIn('<h1 class="mt-5">I\'m sorry you have arrived in no man\'s land.</h1>', html)
