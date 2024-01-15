import tkinter as tk


class Application:
    def __init__(self, http_message_store):
        self.http_message_store = http_message_store

        self.master = tk.Tk()
        self.master.title("HTTP Message Viewer")

        self.text_widget = tk.Text(self.master, wrap="word", height=500, width=500)
        self.text_widget.pack(padx=10, pady=20)

    def update_gui(self):
        if not self.http_message_store.was_updated:
            self.master.after(1000, self.update_gui)
            return

        self.text_widget.delete("1.0", tk.END)

        self.text_widget.tag_configure("message_tag", foreground="red") 

        for message, index in zip(self.http_message_store, range(len(self.http_message_store), 0, -1)):
            self.text_widget.insert(tk.END, f"=========================== Http Message {index} ============================\n", "message_tag")  # Apply the new color tag
            self.text_widget.insert(tk.END, f"Src: {message.ip_src}:{message.port_src} | Dest: {message.ip_dest}:{message.port_dest}\n")
            self.text_widget.insert(tk.END, f"Method: {message.method} | Path: {message.path}\n")
            self.text_widget.insert(tk.END, f"Headers: {message.headers}\n")
            self.text_widget.insert(tk.END, f"Body: {message.body}\n\n\n")

        self.master.after(1000, self.update_gui)

        self.http_message_store.set_updated_false()

    def run(self):
        self.update_gui()  
        self.master.geometry("1280x720")
        self.master.mainloop()