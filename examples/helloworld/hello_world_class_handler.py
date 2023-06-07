from toy.application import Application
from toy.server import HTTPServer
from toy.http import Response
from toy.handlers import Handler

class MyHandler(Handler):
    allowed_methods = ['get']
    def get(self, request):
        return Response('Hello World!', content_type='text/plain')

class MyApp(Application):
    def initialize(self):
        self.add_route(r'/', MyHandler())

server = HTTPServer(MyApp())
server.run()
