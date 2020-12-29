import re
from ._http import HTTPRequest, HTTPResponse


class Route():
    """ Route
    A standard route that calls a HTTPResponse page
    """
    def __init__(self, path, domain=r".*", page=None):
        self.path = path
        self.domain = domain
        self.page = page

        if not callable(page):
            raise TypeError("Page is not callable")
    
    def __call__(self, request):
        if not isinstance(request, HTTPRequest):
            raise TypeError("Request is not HTTPRequest")

        response = self.page(request)
        if isinstance(response, str):
            return HTTPResponse(response)
        elif isinstance(response, HTTPResponse):
            return response
        else:
            raise TypeError("Page did not return a valid response")

class RouteManager():
    routes = []
    not_found = HTTPResponse(
        content="404",
        code=404,
        status="Not Found",
        headers={
            "Content-Type": "text/plain"
        }
    )
    server_error = lambda s, e: HTTPResponse(
        content=f"500\n{e}",
        code=500,
        status="Server Error",
        headers={
            "Content-Type": "text/plain"
        }
    )

    def __init__(self, routes=None, not_found=None, server_error=None):
        self.routes = self.routes or routes
        self.not_found = self.not_found or not_found
        self.server_error = self.server_error or server_error
        

    def __call__(self, request: HTTPRequest):
        for route in self.routes:
            try:
                if (re.fullmatch(route.path, request.path)
                        and re.fullmatch(route.domain, request.domain)):
                    if (r := route(request)): return r
            except Exception as e:
                return self.server_error(e)
        
        return self.not_found
