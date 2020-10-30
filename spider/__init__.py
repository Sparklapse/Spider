from . import web
from ._server import Server, serve
from .web._server import WebServer

__all__ = ['Server', 'WebServer', 'serve', 'web']