import tkinter as TK

class Gui:
    
    #
    # Build the gui
    #
    def __init__(self):

        self.nick = ""
        self.text = ""
        self.running = True

        self.root = TK.Tk()

        self.nick_info = TK.Label(self.root, text = "Your nick:", font = (None, 14))
        self.nick_info.grid(row = 0, column = 0, sticky = "news")

        self.nick_entry = TK.Entry(self.root)
        self.nick_entry.grid(row = 0, column = 1, columnspan = 2, sticky = "news")

        self.nick_button = TK.Button(self.root, text = "Save nick", font = (None, 14), command = self.send_nick)
        self.nick_button.grid(row = 0, column = 3, sticky = "w")


        self.messages_scroll = TK.Scrollbar(self.root)
        self.messages_scroll.grid(row = 1, column = 4, sticky = "news")

        self.messages = TK.Text(self.root, height = 10, width = 50, yscrollcommand = self.messages_scroll.set)
        self.messages.grid(row = 1, column = 0, columnspan = 4)
        self.messages["state"] = "disabled"


        self.message_entry = TK.Entry(self.root)
        self.message_entry.grid(row = 2, column = 0, columnspan = 3, sticky = "news")
        self.message_entry["state"] = "disabled"

        self.message_button = TK.Button(self.root, text = "Send", font = (None, 14), command = self.send_message)
        self.message_button.grid(row = 2, column = 3, sticky = "w")
        self.message_button["state"] = "disabled"

        self.root.resizable(False, False)


    #
    # Start gui
    #
    def start(self):
        self.root.mainloop()
        

    #
    # Set the self.nick as nick and enable writing
    #
    def send_nick(self):
        self.nick = self.nick_entry.get()
        
        self.nick_entry["state"] = "disabled"
        self.nick_button["state"] = "disabled"

        self.message_entry["state"] = "normal"
        self.message_button["state"] = "normal"
        

    #
    # Set the self.text as message and clear entry field
    #
    def send_message(self):
        self.text = self.message_entry.get()
        self.message_entry.delete(0, "end")


    #
    # Adding the message to messages window
    #
    def add_message(self, message):
        self.messages["state"] = "normal"
        self.messages.insert("insert", message+"\n")
        self.messages.see("end")
        self.messages["state"] = "disabled"


    #
    # Exit from gui
    #
    def exit(self):
        self.running = False
        self.root.destroy()
        self.root.quit()
