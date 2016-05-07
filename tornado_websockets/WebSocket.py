import inspect

from six import string_types

from .TornadoWrapper import TornadoWrapper
from .WebSocketHandler import WebSocketHandler
from .exceptions import *


class WebSocket(object):
    def __init__(self, namespace):
        self.events = {}

        self._namespace = namespace.strip()
        if self._namespace[0:1] is not '/':
            self._namespace = '/' + self._namespace

        self._handler = WebSocketHandler
        self._handler.namespaces.update({
            self._namespace: self
        })

        TornadoWrapper.add_handlers([
            ('/ws' + self._namespace, self._handler)
        ])

    def on(self, *args):
        def decorator(func):
            return func

        if len(args) < 1:
            raise ValueError('WebSocket.on decorator take at least one argument.')

        if isinstance(args[0], string_types):
            event = args[0]
            callback = decorator
        elif callable(args[0]):
            event = args[0].__name__
            callback = decorator(args[0])
        elif inspect.isclass(args[0]):
            raise NotImplementedError('WebSocket.on decorator is not already implemented for classes.')
        else:
            raise ValueError('How the f*ck did you use this decorator???')

        if self.events.get(event) is not None:
            raise WebSocketEventAlreadyBinded(
                'The event "%s" is already binded for "%s" namespace' % (event, self._namespace)
            )

        print('-- Binding "%s" event for "%s" namespace' % (event, self._namespace))
        self.events[event] = callback
        return decorator

    def emit(self, *args):

        pass
