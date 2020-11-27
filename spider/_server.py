import sys
import asyncio
import socket
import multiprocessing


class Server():
    def __init__(
            self, service: type = None, max_workers = 10,
            host: str = '', port: int = 8080):

        self.service = getattr(self, 'service', None) or self.service
        self.worker_max = max_workers
        self.worker_able = True if (
                sys.platform.startswith('linux') or 
                sys.platform.startswith('darwin')
            ) else False
        self.host = getattr(self, 'host', None) or host
        self.port = getattr(self, 'port', None) or port

        if self.service == None:
            raise ValueError("No service provided")

        self.start()

    async def _tcp_server(self):
        loop = asyncio.get_running_loop()
        _server = await loop.create_server(
            lambda: self.service(self),
            sock=self.sock
        )

        async with _server:
            await _server.serve_forever()

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

    def serve(self, **kwargs):
        if self.worker_able:
            try:
                self.sock = socket.fromfd(
                    kwargs['sockfn'],
                    family=kwargs['sfamily'], type=kwargs['stype']
                )
            except KeyError:
                raise TypeError(("serve() in current context missing some"
                                 "required argument"))
        else:
            if not self.sock:
                self.sock = socket.socket()
                self.sock.bind((self.host, self.port))

        loop = asyncio.get_event_loop()
        loop.create_task(self._tcp_server())

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.stop()
            loop.run_until_complete(loop.shutdown_asyncgens())

    def create_workers(self):
        if not self.worker_able:
            raise OSError("Unsupported OS! Please serve on a single thread")
        sock = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM
        )
        sock.bind((self.host, self.port))
        sock.setblocking(True)
        sock.set_inheritable(True)

        self.workers = []

        for _ in range(self.worker_max):
            p = multiprocessing.Process(
                target=self.serve,
                args=(
                    sock.fileno(),
                    sock.family,
                    sock.type
                )
            )
            p.start()
            self.workers.append(p)

        while True:
            pass

def serve(server: type):
    print("Serving", server.__name__)
    print("Press Ctrl+C to stop serving")
    _s = server()

    sock = socket.socket()
    sock.bind((_s.host, _s.port))
    _s.sock = sock

    _s.serve()
    print("Closing")
