from toy.application import Application
from toy.http import Response
from toy.server import HTTPServer


def hello_world(request):
    return Response('Hello World!', content_type='text/plain')


class MyApp(Application):
    def initialize(self):
        self.add_route(r'/', hello_world)


server = HTTPServer(MyApp())
server.run()
