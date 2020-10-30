import gzip
from urllib.parse import unquote, parse_qs


class HTTPRequest():
    def __init__(self, request):
        self._request = request.splitlines()[0].split(' ')
        if len(self._request) != 3:
            raise ValueError("Invalid Request")

        self.headers = {}
        _headers = request.split('\r\n\r\n')[0].splitlines()[1:]
        for _h in _headers:
            if ': ' in _h:
                self.headers[_h.split(': ')[0]] = ': '.join(_h.split(': ')[1:])

    @property
    def method(self) -> str:
        """ method
        The method used when making the request
        (eg. GET, POST, DELETE, PUT, etc.)
        """
        return self._request[0]
    
    @property
    def path(self) -> str:
        """ path
        The path of the url
        (eg. /foo/bar)
        """
        return unquote(self._request[1].split('?')[0])
    
    @property
    def params(self) -> dict:
        """ params
        The parameters passed through the url
        (eg. ?foo=bar&car=zar -> {"foo": "bar", "car": "zar"})
        """
        if '?' in self._request[1]:
            return parse_qs(self._request[1].split('?')[1])
        else:
            None

    @property
    def version(self) -> str:
        """ version
        The request version used
        (eg. HTTP/1.1)
        """
        return self._request[2]
    
    @property
    def domain(self) -> str:
        """ domain
        The domain being requested
        (eg. example.com)
        """
        return self.headers['Host'].split(':')[0]
    

class HTTPResponse():
    def __init__(self, content,
                version="HTTP/1.1", code=200, status="OK",
                content_type='text/html', encoding="utf-8", headers={}
            ):
        self.version = version
        self.code = code
        self.status = status
        self.encoding = encoding

        self.headers = {
            "Server": "Spider Web",
            "Content-Type": ' '.join(
                ("text/html;", f"charset={encoding}")
            ),
            **headers
        }

        self.content = content

    # TODO: Create a hash function so you can determine if you can just
    # return a 304 "Not Modified"
    def __hash__(self):
        pass

    def __call__(self):
        _resp ='\r\n'.join((
            f"{self.version} {self.code} {self.status}",
            *[
                ': '.join((str(_), self.headers[_]))
                for _ in self.headers.keys()
            ],
            '\r\n',
            self.content
        ))
        return _resp.encode(self.encoding)
