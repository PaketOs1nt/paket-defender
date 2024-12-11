import socket
import time

with open('config/NOTIFY_SERVER_PORT', 'r') as f:
    NOTIFY_SERVER_PORT = int(f.read())

def notify(text: str):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', NOTIFY_SERVER_PORT))
        time.sleep(0.05)
        sock.send(text.encode())
        time.sleep(0.15)
        sock.close()
    except:
        pass