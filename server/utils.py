from datetime import datetime
from os.path import basename, isdir, isfile, exists, join as path_join
from os import stat, listdir as syslistdir
from pathlib import Path
from platform import platform
from tomllib import loads
from functools import wraps

from flask import redirect, session
from humanize.filesize import naturalsize
from humanize.time import naturaltime


class FileStat:
    """File Stat"""

    def __init__(self, path: str) -> None:
        self._path = path
        self._name = basename(path)
        self._isdir = isdir(path)
        self._isfile = isfile(path)
        if exists(path):
            stated = stat(path)
            self._created = stated.st_ctime
            self._size = stated.st_size
        else:
            self._created = 0
            self._size = -1

    @property
    def path(self):
        """Path of file"""
        return self._path

    @property
    def name(self):
        """Name of file"""
        return self._name

    @property
    def isdir(self):
        """Is file a directory?"""
        return self._isdir

    @property
    def isfile(self):
        """Is file a file?"""
        return self._isfile

    @property
    def base_created_at(self):
        """File created, when?"""
        return self._created

    @property
    def base_size(self):
        """File size or how much contents within directory (excluding child's content)"""
        return self._size

    @property
    def size(self):
        """File size"""
        if self._isdir:
            return str(self.base_size)
        return naturalsize(self._size, True)

    @property
    def created_at(self):
        """File creted, when? (relative)"""
        timed = datetime.fromtimestamp(self.base_created_at)
        return naturaltime(timed, True, when=datetime.now())


def loadtomlfile(file: str | Path):
    with open(file, encoding='utf-8') as io:
        return loads(io.read())


def filter_crumb(path: str):
    return [crumb for crumb in path.split('/') if crumb]


def listdir(cwd=""):
    for file in syslistdir(cwd):
        yield FileStat(path_join(cwd, file))


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("sid", None) is None:
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper


if platform() == "Windows":
    ROOT = Path("C:/")
else:
    # fuck you, i don't care about your system if it isn't UNIX-like or Windows.
    ROOT = Path("/")
