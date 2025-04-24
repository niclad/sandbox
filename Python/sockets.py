import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.running = False
        
    # create a TCP/IP socket
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.running = True
        print(f'Server started on {self.host}:{self.port}')

        # Accept clients in a separate thread
        self.accept_thread = threading.Thread(target=self.accept_clients, daemon=True)
        self.accept_thread.start()

    def accept_clients(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f'Connection from {addr}')
                self.clients.append(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            except OSError:
                break

    def handle_client(self, client_socket):
        with client_socket:
            while self.running:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    print(f'Received: {data.decode()}')
                    client_socket.sendall(f"Recv {data.length} bytes".encode())
                except ConnectionResetError:
                    break
        
        self.clients.remove(client_socket)
        print('Client disconnected')

    def stop(self):
        self.running = False
        for client in self.clients:
            client.close()
        self.server_socket.close()
        print('Server stopped')

if __name__ == "__main__":
    server = Server('127.0.0.1', 65432)
    try:
        server.start()
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        server.stop()

