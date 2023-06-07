from toy.application import Application
from toy.server import HTTPServer
from toy.http import Response

def hello_world(request):
    return Response('Hello World!',content_type='text/plain')

class MyApp(Application):
    def initialize(self):
        self.add_route(r'/', hello_world)

server = HTTPServer(MyApp())
server.run()
