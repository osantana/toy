from .http import Request, Response, WSGIResponse
from .routing import Routes


class Application:
    def __init__(self):
        self.routes = Routes()

    def add_route(self, path, handler):
        self.routes.add_route(path, handler)

    def __call__(self, environ, start_response):
        request = Request(environ)

        # TODO: continue from this point...
        
        status = '200 OK'
        output = b'Hello World!\n'
        response_headers = [('Content-type', 'text/plain'),
                            ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [output]

# process Request
#    method
#    path
#    querystrings
#    headers
#    content
# Application
#    route
#    dispatch
#    return (response or exception)
# process Response
#    status (staty)
#    headers
#    content
