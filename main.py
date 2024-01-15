from application import Application
from http_message_store import HttpMessageStore
from http_sniffer import HttpSniffer


def main():
    http_message_store = HttpMessageStore()

    sniffer = HttpSniffer(http_message_store)
    sniffer.start()

    app = Application(http_message_store)
    app.run()



if __name__ == '__main__':
    main()
    
    