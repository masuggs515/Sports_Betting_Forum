from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, url

class RegisterUserForm(FlaskForm):

    email = StringField("Email", validators=[Email()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class LoginUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class EditUserForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])

    image_url = StringField("Profile Image URL", 
                        default='https://icon-library.com/images/default-profile-icon/default-profile-icon-16.jpg',
                        validators=[url()])

    password = PasswordField("Password", validators=[InputRequired()])

class CommentForm(FlaskForm):

    text = TextAreaField("Comment", validators=[InputRequired()])