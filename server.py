from threading import Thread   
from server_gui import *     
import socket


class Server:
    
    #
    # Setting up the server
    #
    def __init__(self, ip = "localhost", port = 5678):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nicks = []
        self.gui = Gui()


    #
    # Bind the server
    #
    def bind(self):
        self.gui.add_message("[!] bind..")
        self.server.bind((self.ip, self.port))


    #
    # Beginning of listening
    #
    def listen(self):
        self.gui.add_message("[!] listen..")
        self.server.listen()


    #
    # Waiting for new clients
    #
    def accept(self): # Thread
        while True:
            client, address = self.server.accept()
            self.clients.append(client)
            self.gui.add_message("[+] New client detected. Waiting for nick")

            try: # trying of get nick from client
                client.send("/nick".encode("UTF-8"))
                nick = client.recv(1024).decode("UTF-8")
                self.gui.add_message(f"[+] Nick of the new client: {nick}")
                self.nicks.append(nick)

                client_thread = Thread(target = self.get, args = (client,))
                client_thread.start()

                self.send(client, "", "join")
                self.gui.add_message("[+] New client joined")

            except ConnectionResetError: # situation when client break up 
                                         # connection and not send nick
                self.gui.add_message("[-] New client canceled logging")
                self.clients.pop() # client_thread add client to self.clients.
                                   # So despite of except we have to delete him.


    #
    # Sending message to all clients
    #
    def send(self, client, text, message_type):
        try: # "normal" or "join" situation.
            index = self.clients.index(client)
            nick = self.nicks[index]

        except: # "leave" situtation.
            nick = text

        for c in self.clients:
            if message_type == "normal": # client want to say something.
                c.send(f"[>] {nick}: {text}".encode("UTF-8"))

            elif message_type == "join": # client want to join.
                c.send(f"[+] {nick} joined to the chat".encode("UTF-8"))

            elif message_type == "leave": # client want to leave.
                c.send(f"[-] {nick} left the chat".encode("UTF-8"))

        if message_type == "normal": # client want to say something.
            self.gui.add_message(f"[>] {nick}: {text}")

        elif message_type == "join": # client want to join.
            self.gui.add_message(f"[+] {nick} joined to the chat")

        elif message_type == "leave": # client want to leave.
            self.gui.add_message(f"[-] {nick} left the chat")


    #
    # Getting message from client
    #
    def get(self, client): # Thread
        running = True
        while running:
            try: # trying of getting message from the client.
            
                text = client.recv(1024).decode("UTF-8")
                if text == "/bye": # situation when the client want to exit.

                    running = False
                    self.delete_client(client)
                    self.gui.add_message("[!] Client left by /bye")
                    break
                else: # situation when the client want to say something.
                    self.send(client, text, "normal")

            except ConnectionResetError: # situation when server can not 
                                         # connect with client.
                running = False
                self.delete_client(client)
                self.gui.add_message("[-] Client left by sudden disconnection")
                break


    #
    # deleting client from self variables
    #
    def delete_client(self, client):
        try: # situation when client want to exit or server want to delete
             # client who disappeared.
            client.send("/bye".encode("UTF-8"))
            index = self.clients.index(client)
            del self.clients[index]
            nick = self.nicks[index]
            del self.nicks[index]
            self.send(client, nick, "leave")
            

        except ConnectionResetError: # situation when client disappeared.
            self.find_broken_client()


    #
    # Looking for client who broke up connection
    #
    def find_broken_client(self):
        for c in self.clients:
            try: # trying of contact with the client.
                c.send("test".encode("UTF-8"))

            except ConnectionResetError: # error means that the client 
                                         # is not exist.
                index = self.clients.index(c)
                del self.clients[index]
                nick = self.nicks[index]
                self.send(nick, nick, "leave")
                del self.nicks[index]
                self.gui.add_message(f"[+] Broken client {nick} deleted")
                break


    #
    # Run the server
    #
    def start(self):
        self.bind()

        self.listen()

        self.accept_thread = Thread(target = self.accept)
        self.accept_thread.start()
        
        self.gui.start()



server = Server()
server.start()