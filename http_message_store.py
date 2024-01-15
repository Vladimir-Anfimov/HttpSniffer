from typing import Deque
from http_message import HttpMessage
from collections import deque

from http_message_formtter import HttpMessageFormatter

class HttpMessageStore:
    MAX_DEQUE_SIZE = 100

    def __init__(self):
        self.messages: Deque[HttpMessageFormatter] = deque()
        self.was_updated = False

    def add(self, message: HttpMessage):
        if len(self.messages) == HttpMessageStore.MAX_DEQUE_SIZE:
            self.messages.pop()

        self.messages.appendleft(HttpMessageFormatter(message))
        self.was_updated = True


    def __iter__(self):
        return iter(self.messages)
    
    def __len__(self):
        return len(self.messages)
    
    def set_updated_false(self):
        self.was_updated = False