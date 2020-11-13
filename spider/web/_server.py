import logging
import re

from .._server import Server
from ._http import HTTPRequest, HTTPResponse
from ._route import Route
from ._service import WebService


class WebServer(Server):
    service = WebService

    compression = True

    routes = []
    route_not_found = HTTPResponse(
        content="404",
        code=404,
        status="Not Found",
        headers={
            "Content-Type": "text/plain"
        }
    )
    route_server_error = lambda s, e: HTTPResponse(
        content=f"500\n{e}",
        code=500,
        status="Server Error",
        headers={
            "Content-Type": "text/plain"
        }
    )

    def receiver(self, request: HTTPRequest):
        for route in self.routes:
            try:
                if (re.fullmatch(route.path, request.path)
                        and re.fullmatch(route.domain, request.domain)):
                    print(
                        request.method,
                        request.domain,
                        request.path,
                        request.params
                    )

                    if (r := route(request)): return r
            except Exception as e:
                return self.route_server_error(e)
        
        return self.route_not_found
