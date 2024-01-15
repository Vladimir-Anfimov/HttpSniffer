from typing import Deque
from http_message import HttpMessage
from collections import deque

class HttpMessageStore:
    MAX_DEQUE_SIZE = 100

    def __init__(self):
        self.messages: Deque[HttpMessage] = deque()
        self.was_updated = False

    def add(self, message: HttpMessage):
        self.was_updated = True
        if len(self.messages) == HttpMessageStore.MAX_DEQUE_SIZE:
            self.messages.pop()

        self.messages.appendleft(message)


    def __iter__(self):
        return iter(self.messages)
    
    def __len__(self):
        return len(self.messages)
    
    def set_updated_false(self):
        self.was_updated = False