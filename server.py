from dotenv import load_dotenv
import threading
import socket
import os


load_dotenv('.env')


class Server:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.clients = []
        self.nick_names = []

    def bind_and_listen(self) -> None:
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"{self.host} is listening!!!")
    
    def broadcast(self, message: str) -> None:
        for client in self.clients:
            client.send(message)
        
    def handle(self, client) -> None:
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except Exception as e:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                self.nickname = self.nick_names[index]
                self.broadcast(f'{self.nickname} has left the chat!'.encode('ascii'))
                print(f'{self.address} Has Diconnected')
                self.nick_names.remove(self.nickname)
                break
    
    def recieve(self) -> None:
        while True:
            self.client, self.address = self.server.accept()
            print(f"{self.address} Connected")
            self.client.send("NICK".encode('ascii'))
            nickname = self.client.recv(1024).decode('ascii')
            self.nick_names.append(nickname)
            self.clients.append(self.client)

            print(f"Nickname of the client is {nickname}")
            self.broadcast(f"{nickname} joined the chat".encode('ascii'))
            self.client.send('Connected to the server!'.encode('ascii'))
            self.threads()


    def threads(self) -> None:
        thread = threading.Thread(target=self.handle, args=(self.client,))
        thread.start()

    def run(self) -> None:
        self.bind_and_listen()
        self.recieve()
        

        
if __name__=='__main__':
    
    HOST = socket.gethostbyname(socket.gethostname())
    

    Server(HOST, int(os.getenv('PORT'))).run()
