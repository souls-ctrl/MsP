from abc import ABCMeta, abstractmethod
#import inspect
import re



class RESTBase(metaclass=ABCMeta):
    """."""
    def __init__(self, value):
        """."""
        self.value = value
        self.headers = [('Accept', 'text/plain'),
                        ('Content-type', 'application/json; charset=utf-8')]
        self.status = self.get_status()
        '''
        model = self.model()
        if model:
            print(model, 'restbase')
            if not inspect.isclass(model):
                model['__tablename__'] = model['tablename']
                del model['tablename']
                self.table = type(model['__tablename__'], (Model, ), model)
            else:
                self.table = model
        '''

    @abstractmethod
    def get_status(self):
        """."""
        pass

    @abstractmethod
    def whoami(self):
        """."""
        pass

    @abstractmethod
    def controller(self):
        """."""
        pass

    @staticmethod
    def model():
        """."""
        return None
        
    def _get_helpers(self, pattern):
        """."""
        regex = re.compile(pattern)
        match = regex.match(self.value)
        if match:
            return [match.group(ind) for ind in range(regex.groups)]
        return None

    def __call__(self, environ, start_response):
        """."""
        _ = environ
        start_response(self.get_status(), self.headers)
        yield str(self.controller()).encode('utf-8')

    def __str__(self):
        """."""
        return "<%s: %s>" % (self.__class__.__name__, self.value)

    def __repr__(self):
        """."""
        return str(self)
