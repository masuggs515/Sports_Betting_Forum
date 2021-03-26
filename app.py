from flask import Flask, g, render_template, redirect, session, flash, request
from sqlalchemy.exc import IntegrityError
import requests
import json
from models import db, connect_db, User, Game, Comment, Like
from secret import API_KEY
from functions import add_comment, database_add_games
from forms import RegisterUserForm, LoginUserForm, CommentForm, EditUserForm


app = Flask(__name__)
app.config["SECRET_KEY"] = 'bettinggnitteb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sports_forum'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)

res = requests.get(f'https://api.the-odds-api.com/v3/sports/?apiKey={API_KEY}')
all_leagues = json.loads(res.text)

db.create_all()

CURR_USER_KEY = "curr_user"

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """
    Create new user and add to DB. Redirect to leagues page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        return redirect('/leagues')

    form = RegisterUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data
                )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/leagues")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    if CURR_USER_KEY in session:
        return redirect('/leagues')

    form = LoginUserForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Welcome back, {user.username}!", "success")
            return redirect("/leagues")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Logs out user and removes user from session."""
    do_logout()
    flash('Successfully logged out.', 'success')
    """Handle logout of user."""
    return redirect('/login')

@app.route('/')
def home_page():
    if CURR_USER_KEY in session:
        return redirect('/leagues')
    
    return redirect('/signup')

# User page

@app.route('/user/<user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    comments = (Comment.query.filter(Comment.user_id==user.id)
                                    .order_by(Comment.timestamp.desc())
                                    .all())
    return render_template('user_details.html', user=user, comments=comments)

@app.route('/user/<user_id>/edit', methods=["GET", "POST"])
def edit_profile(user_id):
    form = EditUserForm()
    curr_user = User.query.get_or_404(user_id)
    if curr_user.id != g.user.id:
        flash('You can only edit your own profile.', 'danger')
        return redirect('/leagues')
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            curr_user.username = form.username.data
            curr_user.image_url = form.image_url.data
            db.session.commit()
        else:
            flash('Incorrect username or password', 'danger')
            return render_template('edit_user.html', form=form, user=curr_user)
        flash(f"Successfully Edited {curr_user.username}'s Profile", "success")
        return redirect('/leagues')
    else:
        return render_template('edit_user.html', form=form, user=curr_user)
    
@app.route('/user/<user_id>/delete')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == g.user.id:
        do_logout()
        db.session.delete(user)
        db.session.commit()
        return redirect('/signup')
    else:
        flash("You cannot delete another user, here's your profile to edit!", "danger")
        return redirect(f'/user/{user.id}')


# Leagues and games/spreads


@app.route('/leagues')
def leagues_list():
    if all_leagues["success"]:
        league_data = all_leagues["data"]
        return render_template('leagues.html', league_data=league_data)

    else:
        return "There was an issue returning sports data."

@app.route('/leagues/<league>')
def all_games_in_sport(league):
    league_res = requests.get(f' https://api.the-odds-api.com/v3/odds/?apiKey={API_KEY}&sport={league}&region=us&mkt=spreads')
    league_games = json.loads(league_res.text)


    j = database_add_games(league_games)
    if j == 'FAILED NO BETS':
        return redirect('/leagues')

    return render_template('league_games.html', league_games=league_games, league=league)

@app.route('/game/<game_id>', methods=["GET", "POST"])
def game_data_comments(game_id):
    form = CommentForm()
    
    comments= (Comment
                .query
                .filter(Comment.game_id==game_id)
                .order_by(Comment.timestamp.desc())
                .limit(20)
                .all())

    if request.method == "POST":
        if not g.user:
            return ({"error": "You must be logged in to leave a comment."}, 200)
        text = request.json["text"]
        game_id = game_id
        return (add_comment(text, game_id), 200)
    else:
        game = Game.query.get_or_404(game_id)
        return render_template('game.html', game=game, form=form, comments=comments)

@app.route('/comment/<comment_id>/delete', methods=["DELETE"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return ({"success"})



# Likes

@app.route('/comment/add_like', methods=["POST"])
def add_like():
    comment_id = request.json["comment_id"]
    
    new_like = Like(comment_id=comment_id, user_id=g.user.id)
    db.session.add(new_like)
    db.session.commit()
    return ({"success":{"added_like": comment_id}})


@app.route('/comment/remove_like', methods=["POST"])
def remove_like():
    comment_id = request.json["comment_id"]
    like_id_obj = Like.query.filter(Like.comment_id==comment_id, Like.user_id==g.user.id).one()
    like_id = like_id_obj.user_id
    like = Like.query.get_or_404((like_id, comment_id))
    db.session.delete(like)
    db.session.commit()
    return ({"success":{"removed_like": comment_id}})