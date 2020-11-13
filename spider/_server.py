import asyncio
import enum
import gzip
import ssl


class Server():
    service = None

    def __init__(
            self, service: type = None, ssl_ctx=None,
            host: str = '0.0.0.0', port: int = 8080):

        self.service = service or self.service
        self.ssl_ctx = ssl_ctx
        self.host = host
        self.port = port

        if self.service == None:
            raise ValueError("No service provided")

        self.start()

    async def _tcp_server(self):
        loop = asyncio.get_running_loop()
        _server = await loop.create_server(
            lambda: self.service(self),
            self.host, self.port,
            ssl=self.ssl_ctx
        )

        async with _server:
            await _server.serve_forever()

    async def _udp_server(self):
        loop = asyncio.get_running_loop()
        _transport, _protocol = await loop.create_datagram_endpoint(
            lambda: self.service(self),
            local_addr=(self.host, self.port)
        )

        try:
            while loop.is_running():
                await asyncio.sleep(3600)
        finally:
            _transport.close()

    def start(self):
        """ Start
        Called when the server starts.
        """

    def receiver(self, data):
        """ Receiver
        Called whenever the server service receives data.
        """

    def lost(self, exception):
        """ Lost
        Called whenever a connection disconnects or is dropped.
        """

    def serve(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self._tcp_server())
        # loop.create_task(self._udp_server())

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.stop()
            loop.run_until_complete(loop.shutdown_asyncgens())

def serve(server: type):
    print("Serving", server.__name__)
    print("Press Ctrl+C to stop serving")
    _s = server()
    _s.serve()
    print("Closing")
