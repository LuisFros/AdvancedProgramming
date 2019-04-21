import threading
import socket
import pickle
from data import save_songs, ingresar_usuario
import os
import json
from random import choice


class Server:
    def __init__(self, port, host):

        self.host = host
        self.port = port
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_and_listen()
        self.accept_connections()

    def bind_and_listen(self):
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen(5)

    def accept_connections(self):
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
        while True:
            client_socket, _ = self.socket_servidor.accept()
            listening_client_thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket,),
                daemon=True
            )
            listening_client_thread.start()

    @staticmethod
    def send(value, Socket):
        Socket.send(value)

    def listen_client_thread(self, client_socket):
        while True:
            response_bytes_length = client_socket.recv(4)
            response_length = int.from_bytes(response_bytes_length,
                                             byteorder="little")
            response = b""
            while len(response) < response_length:
                response += client_socket.recv(256)
            response_string = response.decode("utf-8")
            self.handle_command(response_string, client_socket)

    def handle_command(self, mensaje, socket):
        first_user = True
        for _ in range(1):
            if "&" in mensaje:
                info = mensaje.split("&")
                sala = info[0]
                first_user = info[1]
                user_name = info[2]
                ingresar_usuario(user_name)
                if sala is None:
                    break
                data = save_songs(sala)
                if first_user:
                    primera = choice(list(data.keys()))
                    cancion = data[primera]
                mensaje = {"header": len(cancion['header']),
                           'body': len(cancion['body'])}
                bytes_mensaje = pickle.dumps(mensaje)
                Server.send(len(bytes_mensaje).to_bytes(4, 'little'),
                            socket)
                Server.send(bytes_mensaje, socket)
                Server.send(cancion['header'], socket)
                Server.send(cancion['body'], socket)


if __name__ == "__main__":
    import sys

    PORT = 7070
    HOST = "localhost"
    try:
        server = Server(PORT, HOST)
    except Exception as err:
        print(err)
    finally:
        sys.exit()
