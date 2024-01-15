import re

class Search:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.regex = re.compile(self.pattern.lower())


    def apply(self, message: str) -> bool:
        return self.regex.search(str(message).lower()) is not None
        

    def applyOnMany(self, messages: list) -> list:
        return list(filter(self.apply, messages))