import logging

# reimplement the NullHandler that does nothing. Not needed in python 2.7+
class NullHandler(logging.Handler):
    def emit(self, record):
        pass

