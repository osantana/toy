from unittest.mock import Mock

from toy.server import HTTPServer


def test_basic_server(application):
    mock_server_class = Mock()
    mock_server_instance = mock_server_class.return_value

    server = HTTPServer(application, wsgi_server=mock_server_class, quiet=True)
    server.run()

    assert server.hostname == 'localhost'
    assert server.port == 8080
    assert server.settings['quiet'] is True
    mock_server_instance.set_app.assert_called_once_with(application)
    mock_server_instance.serve_forever.assert_called_once()


def test_basic_server_string_port(application):
    server = HTTPServer(application, port='9000', quiet=True)
    assert server.port == 9000
