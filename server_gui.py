import tkinter as TK

class Gui:
    
    #
    # Build the gui
    #
    def __init__(self):
        self.root = TK.Tk()
        self.messages_scroll = TK.Scrollbar(self.root)
        self.messages_scroll.grid(row = 0, column = 0, sticky = "news")

        self.messages = TK.Text(self.root, height = 20, width = 50, yscrollcommand = self.messages_scroll.set)
        self.messages.grid(row = 1, column = 0, columnspan = 4)
        self.messages["state"] = "disabled"
        
        self.root.resizable(False, False)


    #
    # Start the gui
    #
    def start(self):
        self.root.mainloop()
        

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

