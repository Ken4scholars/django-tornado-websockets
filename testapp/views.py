from django.views.generic import TemplateView

from tornado_websockets.websocket import WebSocket

ws_chat = WebSocket('/my_chat')
ws_chat_without_history = WebSocket('/my_chat_without_history')

class MyChat(TemplateView):
    """
        Proof of concept about a really simple web chat using websockets and supporting messages history
    """

    template_name = 'testapp/index.html'
    messages = []

    def __init__(self, **kwargs):
        super(MyChat, self).__init__(**kwargs)

        # Otherwise, 'self' parameter for method decorated by @ws_chat.on will not be defined
        ws_chat.context = self

    @ws_chat.on
    def connection(self, socket, data):
        """
            Called when the client send the event "connection".

            :param data: Data sent by a client
            :param socket: WebSocket of the current client
            :type data: dict
            :type socket: tornado_websockets.websockethandler.WebSocketHandler
            :return: None
        """

        [socket.emit('new_message', __) for __ in self.messages]
        ws_chat.emit('new_connection', '%s just joined the webchat.' % data.get('username', '<Anonymous>'))

    @ws_chat.on
    def message(self, socket, data):
        """
            Called when the client send a new message

            :param data: Data sent by a client
            :param socket: WebSocket of the current client
            :type data: dict
            :type socket: tornado_websockets.websockethandler.WebSocketHandler

            :return: None
        """

        message = {
            'username': data.get('username', '<Anonymous>'),
            'message': data.get('message', 'Empty message')
        }

        ws_chat.emit('new_message', message)
        MyChat.messages.append(message)

    @ws_chat.on
    def clear_history(self, socket, data):
        """
            Called when a client wants to clear messages history.
            Used only for client-side JavaScript unit tests
        """

        self.messages = []


@ws_chat_without_history.on
def connection(socket, data):
    ws_chat_without_history.emit('new_connection', '%s just joined the webchat.' % data.get('username', '<Anonymous>'))

@ws_chat_without_history.on
def message(socket, data):
    message = {
        'username': data.get('username', '<Anonymous>'),
        'message': data.get('message', 'Empty message')
    }

    ws_chat_without_history.emit('new_message', message)
