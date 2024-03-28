# Group#: G2
# Student Names: Chinmay Bhide, Alex Gu

from tkinter import *
import socket
import threading

class ChatServer:
    """
    This class implements the chat server.
    It uses the socket module to create a TCP socket and act as the chat server.
    Each chat client connects to the server and sends chat messages to it. When 
    the server receives a message, it displays it in its own GUI and also sents 
    the message to the other client.  
    It uses the tkinter module to create the GUI for the server client.
    See the project info/video for the specs.
    """
    # To implement 
    def __init__(self, window):
        '''
        Building GUI and Server socket
        '''
        # building GUI for server
        self.window = window
        self.configNetworking()
        self.buildGUI()

        self.client_connections = []
        
        '''
        # initializing server socket + port
        self.serverName = '127.0.0.1'   # setting server name: localhost = IP address 127.0.0.1
        self.serverPort = 8080  # setting a port number
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # creating TCP welcoming socket on server
        self.serverSocket.bind((self.serverName, self.serverPort))  # binding server socket to client socket
        self.serverSocket.listen(5) # listening for incoming TCP requests


        # Creating server thread to wait and be ready to accept any connections
        self.server_thread = threading.Thread(target=self.accept_connections)
        self.server_thread.start()
        '''
        print("Server is ready to recieve") # double checking server status

    def configNetworking(self) -> None:
        self.client_connections = []
        

        # initializing server socket + port
        self.serverName = '127.0.0.1'   # setting server name: localhost = IP address 127.0.0.1
        self.serverPort = 8080  # setting a port number
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # creating TCP welcoming socket on server
        self.serverSocket.bind((self.serverName, self.serverPort))  # binding server socket to client socket
        self.serverSocket.listen(5) # listening for incoming TCP requests


        # Creating server thread to wait and be ready to accept any connections
        self.server_thread = threading.Thread(target=self.accept_connections)
        self.server_thread.start()
        
    def buildGUI(self) -> None:
        # Label for chat server
        self.server_label = Label(self.window, text="Chat Server")
        self.server_label.grid(row=0, column=0, sticky=W)

        # Label for Chat history + textbox creation
        self.chat_history_label = Label(self.window, text="Chat History")
        self.chat_history_label.grid(row=2, column=0, sticky=W)
        self.chat_history_text = Text(self.window, height=10, width=40)
        self.chat_history_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=W+E)

    def get_data(self, connectionSocket) -> None:
        while True:
            data = connectionSocket.recv(4096)
            decoded = data.decode('utf-8')
            print(decoded)
            self.chat_history_text.insert(END, f"{decoded}")
            print("In get_data: connectionSocket=" + str(connectionSocket))
            for connection in self.client_connections:
                if connection != connectionSocket:        
                    connection.sendall(decoded.encode('utf-8'))

        
    def accept_connections(self) -> None:
        '''
        Ready to accept connections
        '''
        while True:
            connectionSocket, addr = self.serverSocket.accept()
            self.client_connections.append(connectionSocket)
            print("Accepted connection addr=" + str(addr) + " \n connectionSocket=" + str(connectionSocket))

            threading.Thread(target=self.get_data, args=(connectionSocket,)).start()

    


def main(): #Note that the main function is outside the ChatServer class
    window = Tk()
    ChatServer(window)
    window.mainloop()
    #May add more or modify, if needed

if __name__ == '__main__': # May be used ONLY for debugging
    main()