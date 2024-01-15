import tkinter as tk
from http_message_store import HttpMessageStore
from search import Search

class Application:
    """
    Used to display all the HTTP messages captured by the HttpSniffer. 
    """
    REFRESH_RATE = 1000
    WINDOW_SIZE = "1280x720"


    """
    Initializes the Application object.
    Parameters:
        http_message_store (HttpMessageStore): The store to get the messages from.
    """
    def __init__(self, http_message_store: HttpMessageStore):
        self.initialize_search()
        self.http_message_store = http_message_store

        self.master = tk.Tk()
        self.setup_gui()

    """
    Initializes the Search object with a regex pattern that matches any string.
    """
    def initialize_search(self):
        self.search = Search(".*")
        self.changed_search = True


    def setup_gui(self):
        self.master.title("HTTP Sniffer")

        self.create_search_widgets()
        self.create_informational_text_widget()
        self.create_text_widget()


    def create_search_widgets(self):
        self.search_entry = tk.Entry(self.master, width=500)
        self.search_entry.pack(padx=10, pady=10)

        self.search_button = tk.Button(self.master, text="Search", command=self.run_search)
        self.search_button.pack(padx=10, pady=10)


    def create_informational_text_widget(self):
        self.informational_text = tk.Label(self.master, text="Search for a regex pattern in the HTTP messages")
        self.informational_text.pack(padx=10, pady=10)


    def create_text_widget(self):
        self.text_widget = tk.Text(self.master, wrap="word", height=500, width=500)
        self.text_widget.pack(padx=10, pady=20)


    """
    The list of messages is updated every REFRESH_RATE milliseconds.
    If the list was not updated or the search pattern was not changed, the method is programmed to run again 
    in REFRESH_RATE milliseconds.
    """
    def update_gui(self):
        if not self.http_message_store.was_updated and not self.changed_search:
            self.master.after(Application.REFRESH_RATE, self.update_gui)
            return

        self.clear_text_widget()
        self.configure_message_tag()

        filtered_messages = self.search.apply_on_many(self.http_message_store.messages)

        self.insert_messages_to_text_widget(filtered_messages)

        self.master.after(Application.REFRESH_RATE, self.update_gui)
        self.http_message_store.set_updated_false()
        self.changed_search = False


    def clear_text_widget(self):
        self.text_widget.delete("1.0", tk.END)


    def configure_message_tag(self):
        self.text_widget.tag_configure("message_tag", foreground="red")

    """
    Inserts the HTTP messages to the text widget on multiple lines.
    """
    def insert_messages_to_text_widget(self, filtered_messages):
        for message, index in zip(filtered_messages, range(len(filtered_messages), 0, -1)):
            text_message= "=" * 50 + f"Http Message {index}" + "=" * 50 + "\n"
            self.text_widget.insert(tk.END, text_message, "message_tag")
            for line in message:
                self.text_widget.insert(tk.END, f"{line}\n")


    def run(self):
        self.update_gui()
        self.master.geometry(Application.WINDOW_SIZE)
        self.master.mainloop()

    """
    Runs the regex search on the HTTP messages.
    If the search pattern is empty, the search is initialized to match any string.
    If an invalid regex pattern is given, the informational text is updated to notify the user.
    """
    def run_search(self):
        search_pattern = self.search_entry.get()
        print(f"Search for {search_pattern}")

        if not search_pattern:
            self.initialize_search()
            self.informational_text["text"] = "Search for any regex pattern in the HTTP messages"
        else:
            try:
                self.search = Search(search_pattern)
                self.informational_text["text"] = f"Search for a regex \"{search_pattern}\" in the HTTP messages"
                print(f"I am searching for {search_pattern}")
            except:
                self.informational_text["text"] = "Invalid regex pattern"
                print(f"Invalid regex pattern: {search_pattern}")

        self.changed_search = True
