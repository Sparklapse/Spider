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

        if not isinstance((response := self.page(request)), HTTPResponse):
            raise TypeError("Page did not return a HTTPResponse")

        return response

