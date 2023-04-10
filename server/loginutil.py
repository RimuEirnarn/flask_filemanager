"""Login utils"""

from flask_login import LoginManager, UserMixin
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired
from sqlite_database import op

from .database import database

login_manager = LoginManager()


class User(UserMixin, database.table('users').get_namespace()):  # type: ignore
    def get_id(self):
        return self.name  # type: ignore

    @classmethod
    def get_user(cls, name: str):
        user = database.table('users').select_one({'name': op == name})
        if not user:
            return None
        return cls(**user)


@login_manager.user_loader
def get_user(name: str):
    return User.get_user(name)


class LoginForm(FlaskForm):
    """Login"""
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("Login")
