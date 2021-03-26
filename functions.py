from models import db, connect_db, User, Game, Comment
from flask import flash, g

def database_add_games(league_data):

    for game in league_data["data"]:
        games_in_db = Game.query.get(game["id"])
        
        if games_in_db:
            games_in_db.team_one_odds = game["sites"][0]["odds"]["spreads"]["points"][0]
            games_in_db.team_two_odds = game["sites"][0]["odds"]["spreads"]["points"][1]
        else:
            if len(game["sites"]) == 0:
                flash('Sorry, League has no available data.', 'danger')
                return "FAILED NO BETS"
            team_one_odds = game["sites"][0]["odds"]["spreads"]["points"][0]
            team_two_odds = game["sites"][0]["odds"]["spreads"]["points"][1]
            id = game["id"]
            team_one = game["teams"][0]
            team_two = game["teams"][1]
            game = Game(id=id, team_one=team_one, team_two=team_two, team_one_odds=team_one_odds, team_two_odds=team_two_odds)
            db.session.add(game)
        db.session.commit()

def add_comment(text, game_id):
    comment = Comment(text=text, user_id=g.user.id, game_id=game_id)
    db.session.add(comment)
    db.session.commit()
    username = g.user.username
    user_image = g.user.image_url
    comment_id = comment.id
    comment_time = comment.timestamp.strftime("%d %B %Y %I:%M %p")
    comment_json = {
        "text": text,
        "username": username,
        "user_image": user_image,
        "timestamp": comment_time,
        "comment_id": comment_id
    }
    return comment_json