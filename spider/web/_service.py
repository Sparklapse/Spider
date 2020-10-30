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
                HTTPRequest(data.decode())
            )
        except ValueError:
            # TODO: return a 400 bad request
            pass
        else:
            if callable(response):
                self._transport.write(response())
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
