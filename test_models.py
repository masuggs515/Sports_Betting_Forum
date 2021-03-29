"""User model tests."""
import os
from unittest import TestCase

from models import db, User, Game, Comment, Like
from sqlalchemy import exc


os.environ['DATABASE_URL'] = "postgresql:///sports_forum_test"


from app import app

db.create_all()

class GameModelTestCase(TestCase):
    """Test game model."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        g1 = Game(team_one="TestTeam", team_two="TestTeam2", team_one_odds=1.0, team_two_odds= -1.0)
        game_id1 = 'id123'
        g1.id = game_id1

        g2 = Game(team_one="TestTeam3", team_two="TestTeam4", team_one_odds=11.0, team_two_odds= -11.0)
        game_id2 = 'id22'
        g2.id = game_id2

        db.session.add(g1, g2)
        db.session.commit()

        game_1 = Game.query.get(game_id1)
        game_2 = Game.query.get(game_id2)

        self.game_1 = game_1
        self.game1_id = game_id1

        self.game_2 = game_2
        self.game2_id = game_id2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_add_game(self):
        g = Game(team_one="TestTeam", team_two="TestTeam2", team_one_odds=1.0, team_two_odds= -1.0)
        test_id = 'id1458'
        g.id = test_id
        db.session.add(g)
        db.session.commit()

        test_game = Game.query.get(test_id)

        self.assertEqual(test_game.id, 'id1458')
        self.assertEqual(test_game.team_one, "TestTeam")
        self.assertEqual(test_game.team_two, "TestTeam2")
        self.assertEqual(test_game.team_one_odds, '1.0')
        self.assertEqual(test_game.team_two_odds, '-1.0')
        self.assertEqual(len(test_game.comment), 0)

class CommentModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        g1 = Game(team_one="TestTeam", team_two="TestTeam2", team_one_odds=1.0, team_two_odds= -1.0)
        game_id1 = 'id123'
        g1.id = game_id1

        db.session.add(g1)
        db.session.commit()

        game_1 = Game.query.get(game_id1)

        self.game_1 = game_1
        self.game1_id = game_id1

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_add_comment(self):
        u1 = User.signup("test1","password", "email1@email.com")
        user_id1 = 11
        u1.id = user_id1
        db.session.commit()
        user = User.query.get(user_id1)
        c = Comment(user_id = user.id, game_id = self.game1_id, text="Test Text")
        c.id = 33
        db.session.add(c)
        db.session.commit()
        comment_test = Comment.query.get(33)
        
        self.assertEqual(comment_test.id, 33)
        self.assertEqual(comment_test.text, 'Test Text')

class LikeModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        g1 = Game(team_one="TestTeam", team_two="TestTeam2", team_one_odds=1.0, team_two_odds= -1.0)
        game_id1 = 'id123'
        g1.id = game_id1

        u1 = User.signup("test1","password", "email1@email.com")
        user_id1 = 11
        u1.id = user_id1

        db.session.add(g1, u1)
        db.session.commit()

        game_1 = Game.query.get(game_id1)
        u1 = User.query.get(user_id1)

        self.u1 = u1
        self.uid1 = user_id1

        self.game_1 = game_1
        self.game1_id = game_id1

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_likes(self):
        c = Comment(user_id = self.uid1, game_id = self.game1_id, text="Test Text")
        c.id = 33
        db.session.add(c)
        db.session.commit()

        test_like = Like(user_id=self.uid1, comment_id=c.id)
        test_like.id = 254
        db.session.add(test_like)
        db.session.commit()
        like = Like.query.filter(Like.comment_id==33, Like.user_id==11).one()

        self.assertEqual(like.id, 254)
        self.assertEqual(like.user_id, 11)
        self.assertEqual(like.comment_id, 33)


