from toy.server import HTTPServer
from .recipes import get_app


applicaton = get_app()
server = HTTPServer(applicaton)
server.run()
