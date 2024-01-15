import tkinter as tk

from http_message_store import HttpMessageStore
from search import Search

class Application:
    RERENDER_DELAY = 1000

    def __init__(self, http_message_store: HttpMessageStore):
        self.search = Search(".*")
        self.changed_search = True

        self.http_message_store = http_message_store

        self.master = tk.Tk()
        self.master.title("HTTP Sniffer")

        self.search_entry = tk.Entry(self.master, width=500)
        self.search_entry.pack(padx=10, pady=10)
        self.search_button = tk.Button(self.master, text="Search", command=self.run_search)
        self.search_button.pack(padx=10, pady=10)

        self.informational_text = tk.Label(self.master, text="Search for a regex pattern in the HTTP messages")
        self.informational_text.pack(padx=10, pady=10)

        self.text_widget = tk.Text(self.master, wrap="word", height=500, width=500)
        self.text_widget.pack(padx=10, pady=20)

    def update_gui(self):
        

        if not self.http_message_store.was_updated and not self.changed_search:
            self.master.after(Application.RERENDER_DELAY, self.update_gui)
            return

        self.text_widget.delete("1.0", tk.END)

        self.text_widget.tag_configure("message_tag", foreground="red") 

        filtered_messages = self.search.applyOnMany(self.http_message_store.messages)

        for message, index in zip(filtered_messages, range(len(filtered_messages), 0, -1)):
            self.text_widget.insert(tk.END, f"=========================== Http Message {index} ============================\n", "message_tag") 
            for line in message:
                self.text_widget.insert(tk.END, f"{line}\n")

        self.master.after(Application.RERENDER_DELAY, self.update_gui)

        self.http_message_store.set_updated_false()
        self.changed_search = False

    def run(self):
        self.update_gui()  
        self.master.geometry("1280x720")
        self.master.mainloop()


    def run_search(self):
        print(f"Search for {self.search_entry.get()}")
        if self.search_entry.get() == "":
            self.search = Search(".*")
            self.informational_text["text"] = "Search for any regex pattern in the HTTP messages"
        else:
            try:
                self.search = Search(self.search_entry.get())
                self.informational_text["text"] = f"Search for a regex \"{self.search_entry.get()}\" in the HTTP messages"
                print(f"I am searching for {self.search_entry.get()}")
            except:
                self.informational_text["text"] = "Invalid regex pattern"
                print(f"Invalid regex pattern: {self.search_entry.get()}")

        self.changed_search = True