import re
import asyncio

from ._http import HTTPRequest, HTTPResponse


def ready_response(response, request=None, recurse=False):
    if isinstance(response, HTTPResponse):
        return response.read()
    elif isinstance(response, bytes):
        return response
    elif isinstance(response, str):
        return response.encode()
    elif isinstance(response, int) or isinstance(response, float):
        return str(response).encode()
    elif callable(response) and not recurse:
        _resp = response(request)
        return ready_response(_resp, recurse=True)
    else:
        raise TypeError("Couldn't ready response")

class WebService(asyncio.Protocol):
    def __init__(self, server):
        self.server = server

        if not hasattr(server, 'routes'):
            raise ValueError("No routes set!")

        if 404 not in self.server.routes.keys():
            self.server.routes[404] = HTTPResponse(
                "404: Not Found", code=404, headers={
                    "Content-Type": "text/plain"
                }
            )
        if 500 not in self.server.routes.keys():
            self.server.routes[500] = HTTPResponse(
                "500: Server Error", code=500, headers={
                    "Content-Type": "text/plain"
                }
            )

    def connection_made(self, transport):
        self._transport = transport

    def data_received(self, data):
        request = HTTPRequest(data.decode())

        # Route management
        response = None
        for route in self.server.routes.keys():
            try:
                if (not isinstance(route, int) and 
                        (re.fullmatch(route, request.path))):
                    response = ready_response(
                        self.server.routes[route], request
                    )
                    break
            except Exception as e:
                if isinstance(self.server.routes[500], HTTPResponse):
                    response = ready_response(self.server.routes[500])
                break
        
        if not response:
            if isinstance(self.server.routes[404], HTTPResponse):
                response = ready_response(self.server.routes[404])
        
        self._transport.write(response)
        self._transport.close()

    def connection_lost(self, exc):
        self.server.lost(exc)
