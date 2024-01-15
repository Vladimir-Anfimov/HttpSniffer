from typing import Deque
from http_message import HttpMessage
from collections import deque

from http_message_formtter import HttpMessageFormatter

class HttpMessageStore:
    """
    Used to store the HTTP messages.
    It is used by the Application class to display the messages.
    It can store up to 100 messages.
    """

    MAX_DEQUE_SIZE = 100

    """
    Initializes the deque of messages and a flag to indicate if the deque was updated.
    """
    def __init__(self):
        self.messages: Deque[HttpMessageFormatter] = deque()
        self.was_updated = False


    """
    Adds a message to the deque.
    If the deque is full, the oldest message is removed.
    Args:
        message (HttpMessage): The message to add.
    """
    def add(self, message: HttpMessage):
        if len(self.messages) == HttpMessageStore.MAX_DEQUE_SIZE:
            self.messages.pop()

        self.messages.appendleft(HttpMessageFormatter(message))
        self.was_updated = True

    def set_updated_false(self):
        self.was_updated = False

    def __iter__(self):
        return iter(self.messages)
    
    def __len__(self):
        return len(self.messages)
    
