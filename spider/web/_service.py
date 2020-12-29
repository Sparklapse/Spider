import asyncio

from ._http import HTTPRequest, HTTPResponse


class WebService(asyncio.Protocol):
    def __init__(self, server):
        self.server = server

    def connection_made(self, transport):
        self._transport = transport

    def data_received(self, data):
        try:
            response = self.server.receiver(
                request := HTTPRequest(data.decode())
            )
            if not isinstance(response, HTTPResponse):
                raise TypeError((
                    f"Response was not a HTTPResponse."
                    f"Returned {type(response)}"
                ))
        except ValueError:
            return self.server.route_not_found
        else:
            if callable(response):
                if getattr(self.server, 'compression', None):
                    try:
                        do_compression = \
                            "gzip" in request.headers['Accept-Encoding']
                    except KeyError:
                        do_compression = False
                else:
                    do_compression = False
                
                self._transport.write(response(
                    compression=do_compression
                ))
            else:
                self._transport.abort()
        finally:
            self._transport.close()
    
    # Reserved for HTTP3
    def datagram_received(self, data, addr):
        response = self.server.receiver(
            HTTPRequest(data.decode())
        )

        self.transport.sendto(response(), addr)

    def connection_lost(self, exc):
        self.server.lost(exc)
