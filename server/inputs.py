from typing import Literal
from colorful_string import Combination

TAG = {
    "info": Combination.from_string("fg_Green"),
    "warning": Combination.from_string('fg_Yellow'),
    "error": Combination.from_string('fg_Red')
}
PREFIX = {
    "info": "[/]",
    "warning": "[!]",
    "error": "[x]"
}
Tag = Literal['info'] | Literal['warning'] | Literal['error']


def ask(prompt: str, tag: Tag, when_error: str | None = None) -> str:
    """Task to user about anything"""
    try:
        return input(f"{TAG[tag]('[?]')} {prompt}: ")
    except EOFError:
        raise SystemExit(1)
    except (KeyboardInterrupt, Exception):
        if when_error:
            return ask(when_error, 'error', when_error)
    return ""


def ask_char(prompt: str, tag: Tag, when_error: str | None = None):
    char = ask(prompt, tag, when_error)
    if len(char) == 0:
        return ' '
    if len(char) > 1:
        return ask_char(prompt, 'error', when_error)
    return char[0]


def yesno(prompt: str):
    char = ask_char(f"{prompt} (y/n)", "info")
    if char == 'y':
        return True
    return False
