"""CLI Utils"""
from getpass import getpass, getuser
from typing import Literal

from argh import ArghParser
from sqlite_database import op
from tabulate import tabulate
from werkzeug.security import generate_password_hash

try:
    from .database import database, init
    from .inputs import PREFIX, TAG, ask, yesno
except ImportError:
    from database import database, init
    from inputs import PREFIX, TAG, ask, yesno

Tag = Literal['info'] | Literal['warning'] | Literal['error']
init()
users = database.table("users")
parser = ArghParser()


def prefixer(tag: Tag):
    return TAG[tag](PREFIX[tag])


def prefix_print(string: str, tag: Tag = 'info'):
    print(TAG[tag](f"{PREFIX[tag]}"), string)


def map_error(exc: Exception):
    return f"{type(exc).__name__}: {str(exc)}"


def reset():
    """Reset database"""
    database.delete_table('users')
    init()
    prefix_print("Database cleared!")


def create_user():
    """Create user"""
    uname_usage = yesno("Would you use your username?")
    username = getuser() if uname_usage else ask("Username", 'info')
    password = getpass(f'{prefixer("info")} Password: ')
    try:
        users.insert({
            'name': username,
            'password': generate_password_hash(password)
        })
        prefix_print("User created!")
    except Exception as exc:
        prefix_print(f"Cannot create user! {map_error(exc)}", 'error')


def delete_user():
    """Delete user"""
    uname_usage = yesno("Would you use your username?")
    username = getuser() if uname_usage else ask("Username", 'info')
    try:
        users.delete({
            'name': op == username
        })
        prefix_print("User deleted!")
    except Exception as exc:
        prefix_print(f"Cannot delete user! {map_error(exc)}", 'error')


def map_user():
    """Display all users, all password is stripped."""
    header = ('name', 'password')
    allusers = users.select()
    table: list[tuple[str, str]] = []
    if len(allusers) == 0:
        prefix_print("No users available from database!", 'error')
        return
    for user in allusers:
        table.append((user.name, '(hashed)'))
    print(tabulate(table, header, "simple_grid"))


parser.add_commands([reset, create_user, delete_user, map_user])
