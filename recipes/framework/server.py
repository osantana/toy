from wsgiref.simple_server import WSGIRequestHandler, WSGIServer


class HTTPServer:
    def __init__(self, application, wsgi_server=WSGIServer, **kwargs):
        self.application = application

        self.settings = {
            'hostname': 'localhost',
            'port': 8080,
            'quiet': False,
        }
        self.settings.update(kwargs)

        self._wsgi_server = wsgi_server

    @property
    def hostname(self):
        return self.settings['hostname']

    @property
    def port(self):
        return int(self.settings['port'])

    def _print(self, msg):
        if self.settings['quiet']:
            return

        print(msg)

    def run(self):
        server = self._wsgi_server(
            (self.hostname, self.port),
            WSGIRequestHandler,
        )
        server.set_app(self.application)

        self._print(f"Serving on {self.hostname}:{self.port} (press ctrl-c to stop)...")

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            self._print("\nStopping...")
