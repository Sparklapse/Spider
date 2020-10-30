from ._http import HTTPResponse

def render(file: str, **kwargs):
    with open(file, 'r') as html:
        return HTTPResponse(html.read(), **kwargs)
