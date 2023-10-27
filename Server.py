# Server.py

import socket
import math

class MainServer:
    def __init__(self, host, port, max_clients):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.clients = []

    def start(self):
        # Create a server socket and listen for client connections
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(self.max_clients)

        print(f"Server is listening for connections (expecting: {self.max_clients} clients)...")
        # After all the clients connect - we start sending them to work
        while len(self.clients) < self.max_clients:
            client_socket, _ = server_socket.accept()
            self.clients.append(client_socket)
            print(f"New client connected: {client_socket.getpeername()}")

        print("All clients have connected. Distributing work.")

    def listen_for_results(self):
        # Listen for incoming data from the clients
        while True:
            for client in self.clients:
                try:
                    data = client.recv(1024).decode()
                    if len(data) >0:
                        self.handle_client_results(client, data)
                except Exception as e:
                    print(f"An error has occurred receiving data:  {str(e)}")
                    pass


    def handle_client_results(self, client_socket, result):
        # Process the result received from the client
        print(f"Update received from {client_socket.getpeername()}: {result}")


    def send_data(self, client_socket, data):
        # Sending data to a aclient
        try:
            client_socket.send(data.encode())
        except Exception as e:
            print(f"Error sending data to {client_socket.getpeername()}: {str(e)}")


    def distribute_work(self, work_range, encrypted_message):
        # Divide the work_range equally among connected clients
        start_at = math.pow(10, work_range - 1)
        end_at = 0
        jump_buffer = (10 ** work_range) // len(self.clients)

        for client in self.clients:
            end_at += jump_buffer
            range_of_number = f"{int(start_at)}-{int(end_at - 1)}-{encrypted_message}"
            self.send_data(client, range_of_number)
            start_at = end_at

    def start_cracking(self):
        # Gathers the necessary info for the program to start cracking
        print("To start cracking please enter the following")
        encrypted_message = input("MD5 message: ")
        work_range = int(input("Digits: "))
        self.distribute_work(work_range, encrypted_message.lower())


if __name__ == "__main__":
    print("Welcome please enter the amount of clients that will be used")
    max_clients = int(input("Clients to use: "))
    server = MainServer('0.0.0.0', 12345,max_clients)
    server.start()
    server.start_cracking()
    server.listen_for_results()

