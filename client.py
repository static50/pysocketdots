import socket
import pygame
import threading
import time
import struct

PORT = 5052
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

CLIENT_ID = None

BACKGROUND_COLOR = (30, 32, 38)

def receive(client_states):
    request_bytes = 12
    buffer = b""

    while True:
        buffer += client.recv(request_bytes)
        request_bytes = 12 - len(buffer)

        if request_bytes == 0:
            client_id, x, y = struct.unpack("!iff", buffer)
            client_states[client_id] = [x, y]
            request_bytes = 12
            buffer = b""

def send(message):
    client.sendall(message)

def get_client_ID(client_states):
    buffer = b""
    request_bytes = 12

    while True:
        buffer += client.recv(request_bytes)
        request_bytes = 12 - len(buffer)

        if request_bytes == 0:
            client_id, x, y = struct.unpack("!iff", buffer)
            break

    client_states[client_id] = [x, y]
    return client_id

def main():
    client_states = {}

    CLIENT_ID = get_client_ID(client_states) # Start a handshake to get the client ID

    thread = threading.Thread(target=receive, args=(client_states,)) # Start receiving messages from the server
    thread.start()
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    screen.fill(BACKGROUND_COLOR)

    running = True
    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.fill(BACKGROUND_COLOR)
        dt = clock.tick(60) / 1000

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            client_states[CLIENT_ID][1] -= (100 * dt)
            data = struct.pack("!iff", CLIENT_ID, client_states[CLIENT_ID][0], client_states[CLIENT_ID][1])
            send(data)
        elif keys[pygame.K_s]:
            client_states[CLIENT_ID][1] += (100 * dt)
            data = struct.pack("!iff", CLIENT_ID, client_states[CLIENT_ID][0], client_states[CLIENT_ID][1])
            send(data)
        elif keys[pygame.K_a]:
            client_states[CLIENT_ID][0] -= (100 * dt)
            data = struct.pack("!iff", CLIENT_ID, client_states[CLIENT_ID][0], client_states[CLIENT_ID][1])
            send(data)
        elif keys[pygame.K_d]:
            client_states[CLIENT_ID][0] += (100 * dt)
            data = struct.pack("!iff", CLIENT_ID, client_states[CLIENT_ID][0], client_states[CLIENT_ID][1])
            send(data)

        draw_all(screen, client_states)
        pygame.display.flip()

    pygame.quit()

def draw_all(screen, client_states):
    for client in client_states.values():
        pygame.draw.circle(screen, "blue", (client[0], client[1]), 20)


if __name__ == "__main__":
    main()

