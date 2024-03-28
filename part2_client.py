# Group#: G2
# Student Names: Chinmay Bhide, Alex Gu

from tkinter import *
import socket
import threading
from multiprocessing import current_process #only needed for getting the current process name

class ChatClient:
    """
     - This class implements the chat client.
     - It uses the socket module to create a TCP socket and to connect to the server.
     - It uses the tkinter module to create the GUI for the chat client.
    """

    def __init__(self, window):
        # Creating and GUI and writing the  initial networking code
        self.window = window
        self.configNetworking()
        self.buildGUI()
      
    def configNetworking(self) -> None:
        '''
        Helper Function to be used within __init__ -> Configures all the networking (socket creation, connection, etc)
        '''
        #initalizing client socket + ports
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating socket for client
        self.server_ip = '127.0.0.1'                                    
        self.server_port = 8080                                    
        self.client_socket.connect((self.server_ip, self.server_port))  

        # binding "Return" key to send chat messages
        self.window.bind('<Return>', self.sendMessage)

        # create client thread to take message requests
        self.client_thread = threading.Thread(target=self.recvMessage)
        self.client_thread.start()

        self.current_process_name = current_process().name
        self.current_process_port = self.client_socket.getsockname()[1]


    def buildGUI(self) -> None:
        '''
        Helper Function to be used within __init__ -> Sets up all the tkinter objects needed for the the Client side GUI
        '''

        # Label for client # + port #
        self.client_label = Label(self.window, text=f"{self.current_process_name} @port{self.current_process_port}")
        self.client_label.grid(row=0, column=0, sticky=W)

        # Label for chat message + creation of entry box
        self.chat_message_label = Label(self.window, text="Chat message ")
        self.chat_message_label.grid(row=1, column=0, sticky=W)
        self.chat_message_entry = Entry(self.window)
        self.chat_message_entry.grid(row=1, column=1, sticky=W)

        # Label for chat history + creation of text box
        self.chat_history_label = Label(self.window, text="Chat History")
        self.chat_history_label.grid(row=2, column=0, sticky=W)
        self.chat_history_text = Text(self.window, height=10, width=40)
        self.chat_history_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=W+E)

    def recvMessage(self) -> None:
        '''
        Recieves message from server and inserts into Chat History
        '''
        while True:
            msg = self.client_socket.recv(4096).decode("utf-8")
            self.chat_history_text.insert(END, f"{msg}")

    def sendMessage(self, event) -> None:
        '''
        Client message to the server
        '''
        clientMessage = self.chat_message_entry.get()
        if len(clientMessage) > 0:
            # self.client_socket.send(clientMessage.encode('utf-8'))
            self.client_socket.send((f"{self.current_process_name}: {clientMessage} \n").encode('utf-8'))
            self.chat_message_entry.delete(0, END) # wipe variable for new message to be entered in GUI
            self.chat_history_text.insert(END, f"         {self.current_process_name}: {clientMessage} \n") # inserts message at the end of the last written text

            


def main(): #Note that the main function is outside the ChatClient class
    window = Tk()
    c=ChatClient(window)
    # ChatClient(window)
    window.mainloop()
    #May add more or modify, if needed 

if __name__ == '__main__': # May be used ONLY for debugging
    main()