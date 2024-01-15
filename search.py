import re

class Search:
    """
    Search class is used to search for a pattern in a message.
    It is used by the Application class to filter the messages.
    """
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.regex = re.compile(self.pattern.lower())

    """
    Apply the regex search on the given message.
    Args:
        message (str): The message to search.
    Returns:
        bool: True if the regex pattern is found in the message, False otherwise.
    """    
    def apply(self, message: str) -> bool:
        return self.regex.search(str(message).lower()) is not None
        

    """
    Apply the regex search on the given list of messages.
    Args:
        messages (list): The list of messages to search.
    Returns:
        list: The list of messages that match the regex pattern.
    """
    def apply_on_many(self, messages: list) -> list:
        return list(filter(self.apply, messages))