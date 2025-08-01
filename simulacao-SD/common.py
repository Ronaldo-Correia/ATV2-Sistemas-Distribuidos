import threading
import time
import socket

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def criar_socket(porta):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", porta))
    s.listen()
    return s
