import mimetypes
import os
import re

from ._http import HTTPRequest, HTTPResponse


class StaticDeliverer():
    def __init__(
            self, prefix=None, domain=r".*",
            src="./"):
        
        self.path = f"^/{prefix}/.*$" if prefix else "^/.*$"
        self.domain = domain
        self.src = src

        mimetypes.init()

    def __call__(self, request):
        req_file = os.path.join(
            self.src, re.sub(self.path.rstrip('.*$'), '', request.path)
        )

        if not os.path.exists(req_file):
            return None

        f = open(req_file, 'r')
        mime = mimetypes.guess_type(request.path)[0]

        if not mime:
            raise TypeError(f"Was unable to interpret mimetype of {req_file}")

        return HTTPResponse(
            f.read(), content_type=mime
        )
