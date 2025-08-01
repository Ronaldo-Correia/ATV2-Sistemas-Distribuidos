import socket
import threading
import time
from common import log

PORTA = 5001
VIZINHOS = [5002, 5003]  # processo2 e processo3
clock = 0
lock = threading.Lock()

def atualizar_relogio(recebido):
    global clock
    with lock:
        clock = max(clock, recebido) + 1
        log(f"[P1] Mensagem recebida. Relógio atualizado para {clock}")

def servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", PORTA))
    s.listen()
    while True:
        conn, _ = s.accept()
        data = conn.recv(1024).decode()
        if data:
            recebido = int(data.split(":")[1])
            atualizar_relogio(recebido)
        conn.close()

def enviar_mensagem():
    global clock
    while True:
        time.sleep(5)  # envia a cada 5 segundos
        for porta in VIZINHOS:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(("localhost", porta))
                    with lock:
                        clock += 1
                        mensagem = f"P1:{clock}"
                        s.sendall(mensagem.encode())
                        log(f"[P1] Enviou para P{porta-5000} com clock {clock}")
            except Exception as e:
                log(f"[P1] Falha ao enviar para porta {porta}: {e}")

if __name__ == "__main__":
    log("[P1] Iniciando processo")
    threading.Thread(target=servidor, daemon=True).start()
    enviar_mensagem()
