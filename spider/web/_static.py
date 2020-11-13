import mimetypes
import pathlib
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
        print(
            Warning((
                "You should only use the static deliverer for debugging!\n"
                "Use something like nginx instead. You have been warned!"
            ))
        )

    def __call__(self, request):
        req_file = pathlib.PurePath(
            self.src, re.sub(self.path.rstrip('.*$'), '', request.path)
        ).as_posix()

        if not pathlib.Path(req_file).is_file():
            return None

        with open(req_file, 'rb') as f:
            mime = mimetypes.guess_type(request.path)[0]

            if not mime:
                raise TypeError(f"Was unable to interpret mimetype of {req_file}")

            return HTTPResponse(
                f.read(), content_type=mime
            )
