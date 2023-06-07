from toy import application, fields, handlers, resources
from toy.server import HTTPServer


class MyResource(resources.Resource):
    fields = [fields.CharField('name', max_length=255)]

    @classmethod
    def do_get(cls, request, app_args):
        return cls(name='World')


class MyHandler(handlers.ResourceHandler):
    allowed_methods = ['get']
    resource_type = MyResource


class MyApp(application.Application):
    def initialize(self):
        self.add_route(r'/', MyHandler())


server = HTTPServer(MyApp())
server.run()
