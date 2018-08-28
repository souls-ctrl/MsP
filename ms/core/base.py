import importlib
import re
from ms.core.storage import SQLStorage


class RequestMethod:
    """."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    ALL_METHODS = [GET, POST, PUT, DELETE]


class Route:
    """."""
    def __init__(self, pattern, path_app):
        """."""
        self.pattern = '^' + pattern.strip('/').strip('^').strip('$') + '$'
        self.path_app = path_app
        self.app = self._get_controller()
        self.method = self.app.whoami()
        self.model = self.app.model()

    def _get_controller(self, sep='.'):
        """."""
        module, controller = self.path_app.rsplit(sep, maxsplit=1)
        module = importlib.import_module(module)
        class_ = getattr(module, controller)
        inst_class = class_(self.pattern)
        return inst_class


class ApplicationHandler:
    """."""
    def __init__(self, *routes):
        """."""
        self.routes = routes

    def add_route(self, *args):
        """."""
        if len(args) > 1:
            route = Route(args[:-1], methods=args[-1])
            self.routes.append(route)
        elif len(args) == 1:
            self.routes.append(args[0])

    def resolve(self, method, path):
        """."""
        for route in self.routes:
            if method == route.method:
                regex = re.compile(route.pattern)
                print(route.pattern, path, 'resolve')
                match = regex.match(path)
                if match:
                    rest = regex.sub("", path)
                    app = route.app
                    return (app, rest, match)

        return None

    def build_db(self, db_uri):
        """."""
        models = list(set([route.model for route in self.routes if route.model]))
        tables = [model.to_table() for model in models]
        with SQLStorage(db_uri) as db:
            db.create_tables(tables)

    def __call__(self, environ, start_response, path=None):
        """."""
        if path is None:
            path = environ['PATH_INFO']

        path = path.strip('/')
        method = environ['REQUEST_METHOD']
        print(path, '__call__')
        app, rest, match = self.resolve(method, path)
        print(match)
        if app is not None:
            kwargs = match.groupdict()
            if kwargs:
                args = ()
            else:
                kwargs = {}
                args = match.groups()

            environ['wsgiorg.routing_args'] = (args, kwargs)
            if isinstance(app, Route):
                return app(environ, start_response, path=rest)
            else:
                return app(environ, start_response)

