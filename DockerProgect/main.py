import time
import socket
from sklearn.datasets import load_iris
import pandas as pd

data = load_iris()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 7777))
server.listen()

while True:
    client, addr = server.accept()
    try:
        print(f'connection from {addr}')
        client.send('You are now connected:\n'.encode())
        client.send(f"this is your data\n{data['data'][: ,0]}\n".encode())
        client.send(f"this is your data :) \n".encode())
        time.sleep(2)
        client.send('You are being disconnected\n'.encode())
    except BrokenPipeError:
        print(f"Connection lost with {addr}")
    finally:
        client.close()
