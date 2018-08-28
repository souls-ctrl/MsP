
from ms.rest import GET

class Welcome(GET):
    """."""
    def __init__(self, value):
        """."""
        super().__init__(value)

    def controller(self):
        """."""
        return "Welcome! Please, expose your API Rest"

