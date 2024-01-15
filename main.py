from application import Application
from http_message_store import HttpMessageStore
from http_sniffer import HttpSniffer


class Main():
    """
    This class represents the main entry point of the program.
    It initializes the HttpMessageStore, HttpSniffer, and Application objects,
    and provides a method to run the program.
    """

    def __init__(self):
        self.http_message_store = HttpMessageStore()
        self.sniffer = HttpSniffer(self.http_message_store)
        self.app = Application(self.http_message_store)

    def run(self):
        """
        Starts the HttpSniffer and runs the Application GUI Tkinter
        """
        self.sniffer.start()
        self.app.run()


if __name__ == '__main__':
    main = Main()
    main.run()
    
    