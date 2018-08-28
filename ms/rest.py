from ms.core.abstract import RESTBase
from ms.core.base import RequestMethod
import importlib


class GET(RESTBase):
    """."""
    def __init__(self, value):
        """."""
        super().__init__(value)

    def get_status(self):
        """."""
        return "200 OK"

    def whoami(self):
        return RequestMethod.GET

class POST(RESTBase):
    """."""
    def __init__(self, value):
        """."""
        super().__init__(value)

    def get_status(self):
        return "201"

    def whoami(self):
        """."""
        return RequestMethod.POST

class PUT(RESTBase):
    """."""
    def __init__(self, value):
        """."""
        super().__init__(value)

    def get_status(self):
        return "TODO"

    def whoami(self):
        """."""
        return RequestMethod.PUT

class DELETE(RESTBase):
    """."""
    def __init__(self, value):
        """."""
        super().__init__(value)

    def get_status(self):
        return "TODO"

    def whoami(self):
        """."""
        return RequestMethod.DELETE

class REST(RESTBase):
    """."""
    def __init__(self, value, method):
        """."""
        self._request = self._get_request(value, method)
        super().__init__(value)
        print(self._request)
        

    def _get_request(self, value, method):
        """."""
        if method not in RequestMethod.ALL_METHODS:
            raise "TODO µs.rest.REST"

        module = importlib.import_module(__name__)
        class_ = getattr(module, method)
        return class_(value)

    def get_status(self):
        return self._request.get_status()

    def whoami(self):
        """."""
        return self._request.whoami()

if __name__ == '__main__':
    get_method = REST("/Produits", method=RequestMethod.GET)
    print(get_method)
