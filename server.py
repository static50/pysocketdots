import socket
import pygame
import threading
import time
import struct
import random

PACKET_SIZE = 12
PORT = 5052
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

client_states = {} # client id : [x, y]
client_connections = {} # client id : socket object

def handle_client(conn, addr, client_id, client_states):

    print(f"[NEW CONNECTION] {addr} connected with [CLIENT ID] {client_id}")
    request_bytes = 12
    buffer = b""

    while True:
        received_bytes = conn.recv(request_bytes)

        if not received_bytes:
            break

        buffer += received_bytes
        request_bytes = 12 - len(buffer)

        if request_bytes == 0:
            client_id, x, y = struct.unpack("!iff", buffer)
            client_states[client_id] = [x, y]

            request_bytes = 12
            buffer = b""
            update_clients()

    conn.close()

def update_clients(): # broadcasts client_states to all client_connections
    for ID, client_socket in client_connections.items(): # UPDATE CLIENT 1, ... N AND GET THEIR SOCKETS
        for client_id in client_connections.keys():

            new_client_state = struct.pack("!iff", client_id, client_states[client_id][0], client_states[client_id][1])
            client_socket.sendall(new_client_state)

def give_client_state(client_id, conn):
    client_states[client_id] = [random.randint(1, 800), random.randint(1,  600)]
    initial_state = struct.pack("!iff", client_id, client_states[client_id][0], client_states[client_id][1])
    conn.sendall(initial_state)

def start():
    server.listen()
    client_id = 0

    print(f"Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        client_id += 1
        give_client_state(client_id, conn)
        client_connections[client_id] = conn
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_id, client_states))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


start()