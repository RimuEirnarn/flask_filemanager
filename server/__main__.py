"""Server CLI"""
try:
    from .cli import parser
except ImportError:
    from cli import parser

if __name__ == '__main__':
    parser.dispatch()

__all__ = []
