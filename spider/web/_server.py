import re
import importlib

from .._server import Server
from ._http import HTTPRequest, HTTPResponse
from ._service import WebService
from ._route import Route

class WebServer(Server):
    service = WebService

    apps = []

    routes = []
    end_route = HTTPResponse(
        content="404",
        code=404,
        status="Not Found"
    )

    def start(self):
        for app in self.apps:
            a = importlib.import_module(app)
            for r in list(filter(
                        lambda i: isinstance(getattr(a, i), Route),
                        dir(a)
                    )):
                route = getattr(a, r)
                self.routes.append(route)

    def receiver(self, request: HTTPRequest):        
        for route in self.routes:
            if (re.fullmatch(route.path, request.path)
                and re.fullmatch(route.domain, request.domain)
                    ):
                print(
                    request.method,
                    request.domain,
                    request.path,
                    request.params
                )
                return route(request)
        
        return self.end_route
