import json
import gzip
from urllib.parse import unquote, parse_qs


class HTTPRequest():
    def __init__(self, request, host: str):
        self._request = request.splitlines()[0].split(' ')
        if len(self._request) != 3:
            raise ValueError("Invalid Request")

        self._host = host or ""

        self.headers = {}
        self.content = '\r\n\r\n'.join(request.split('\r\n\r\n')[1:])
        _headers = request.split('\r\n\r\n')[0].splitlines()[1:]
        for _h in _headers:
            if ': ' in _h:
                self.headers[_h.split(': ')[0].lower()] = \
                    ': '.join(_h.split(': ')[1:])

    def __repr__(self):
        return f"{self.method} {self.host} {self.path}"

    @property
    def json(self) -> dict or list:
        try:
            return json.loads(self.content)
        except:
            return {}

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
    def file(self) -> str:
        return unquote(self._request[1].split('?')[0].split('/')[-1])

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
    def host(self) -> str:
        """ host
        The host being requested
        (eg. example.com)
        """
        if hasattr(self.headers, 'host'):
            return self.headers['host'].split(':')[0]
        else:
            return self._host
    

class HTTPResponse():
    compression_level = 5

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
            "Content-Type": content_type,
            **headers
        }
        
        if not self.headers['Content-Type'].endswith(';'):
            self.headers['Content-Type'] += ';'

        self.headers['Content-Type'] = ' '.join(
            (self.headers['Content-Type'], f"charset={encoding}")
        )

        self.content = content

    def __call__(self, compression=False):
        if compression:
            self.headers['Content-Encoding'] = "gzip"
            if isinstance(self.content, str):
                content = gzip.compress(
                    self.content.encode(self.encoding),
                    self.compression_level
                )
            elif isinstance(self.content, bytes):
                content = gzip.compress(self.content, self.compression_level)
            else:
                raise TypeError((
                    "Content is not bytes or a str."
                    f"Type is {type(self.content)}"
                ))
        else:
            if isinstance(self.content, str):
                content = self.content.encode(self.encoding)
            else:
                content = self.content

        
        _resp ='\r\n'.join((
            f"{self.version} {self.code} {self.status}",
            *[
                ': '.join((str(_), self.headers[_]))
                for _ in self.headers.keys()
            ],
            '\r\n'
        ))

        response = _resp.encode(self.encoding) + content

        return response

    def __repr__(self):
        return f"{self.headers['Content-Type']} {self.code} {self.status}"
