"""Database"""

from sqlite_database import Database, text
from secrets import token_urlsafe

database = Database("main.db")


def init():
    if not database.check_table('users'):
        database.create_table("users", [
            text("name").primary(),
            text('password')
        ])
