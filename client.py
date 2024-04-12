import socket
import threading
import os


class Client:
    def __init__(self, server_ip, server_port, nickname:str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = server_ip
        self.server_port = server_port
        self.nickname = nickname
    
    def connect(self) -> None:
        self.client.connect((self.server_ip, self.server_port))

    def receive(self) -> None:
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    print(message)
            except Exception as e:
                print('An error occurred')
                self.client.close()
                break

    def send_message(self) -> None:
        while True:
            message = f'{self.nickname}: {input("Message: ")}'
            self.client.send(message.encode('ascii'))

    def threads(self) -> None:
        receive_msg_thread = threading.Thread(target=self.receive)
        receive_msg_thread.start()
        send_msg_thread = threading.Thread(target=self.send_message)
        send_msg_thread.start()

    def run(self) -> None:
        self.connect()
        self.threads()


if __name__=='__main__':
    server_ip = socket.gethostbyname(socket.gethostname())
    server_port = 56666

    client = Client(server_ip, int(server_port), input('Enter Nickname: '))
    client.run()