from toy.application import Application
from toy.handlers import Handler
from toy.http import Response
from toy.server import HTTPServer


class MyHandler(Handler):
    allowed_methods = ['get']

    def get(self, request):
        return Response('Hello World!', content_type='text/plain')


class MyApp(Application):
    def initialize(self):
        self.add_route(r'/', MyHandler())


server = HTTPServer(MyApp())
server.run()
