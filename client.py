from threading import Thread
from client_gui import *
import socket
import sys

class Client:
    
    #
    # Setting up the client
    #
    def __init__(self, host = "localhost", port = 9999):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bufor = 1024
        self.message = ""
        self.gui = Gui()
    
    
    #
    # Trying of connect with server
    #
    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            return True
        except:
            return False


    # 
    # Sending message to server
    #
    def send_message(self, text):
        text = text.encode("UTF-8")
        self.socket.sendall(text)


    #
    # Getting message from server
    #
    def get_message(self): # Thread
        while True:
            text = self.socket.recv(self.bufor)
            text = text.decode("UTF-8")

            if text == "/bye": # acceptance from the server for 
                               # safe connection termination
                self.exit()
                break

            elif text == "/nick": # nickname request
            
                while True: # waiting for nick
                    if self.gui.nick != "":
                        text = self.gui.nick
                        break
                self.send_message(text)

            else: # message from another clients
                self.gui.add_message(text)


    #
    # Checking if the client want to send a message
    #
    def send(self):
        while True:
            if self.gui.text != "": # if message is not empty
                self.send_message(self.gui.text)
                self.gui.text = ""


    #
    # Close connection and program
    #
    def exit(self):
        self.gui.exit()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        sys.exit()


    #
    # Start the client
    #
    def start(self):
        if not self.connect():
            self.gui.add_message("[-] Connection failed")
        else:
            self.gui.add_message("[+] Connection successful")
            self.gui.add_message("[!] Set your nick")
            
            self.getting = Thread(target = self.get_message)
            self.getting.start()

            self.sending = Thread(target = self.send)
            self.sending.start()

        self.gui.start()
            

client = Client(port = 5678)
client.start()