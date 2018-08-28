from ms.core.base import Route
from ms.core.base import ApplicationHandler


class Microservice:
    """."""
    def __init__(self, **kwargs):
        """."""
        self.host = kwargs.get('host', '0.0.0.0')
        self.port = kwargs.get('port', 8080)
        self.access_method = kwargs.get('access_method', ['REST'])
        routes = kwargs.get('routes',
                            [('', 'ms.base.get_started.Welcome')])
        routes = [Route(*args) for args in routes]

        self.application = ApplicationHandler(*routes)
        if kwargs.get('database_uri'):
            db_uri = kwargs.get('database_uri')
            self.application.build_db(db_uri)

    def start(self):
        """."""
        from wsgiref.simple_server import make_server
        server = make_server(self.host, self.port, self.application)
        print("Microservice running on {}:{}".format(self.host, self.port))
        server.serve_forever()
