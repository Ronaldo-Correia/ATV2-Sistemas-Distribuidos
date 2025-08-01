import socket
import threading
import time
from common import log

PORTA = 5001
VIZINHOS = [5002, 5003]
clock = 0
contador_eventos = 0
lock = threading.Lock()

# Snapshot state
snapshot_iniciado = False
snapshot_estado_local = None
snapshot_mensagens_em_transito = []
marcadores_recebidos = set()

def atualizar_relogio(recebido):
    global clock
    with lock:
        clock = max(clock, recebido) + 1

def registrar_evento(tipo, origem_destino=None):
    global clock, contador_eventos

    with lock:
        contador_eventos += 1
        clock += 1
        if tipo == "envio":
            log(f"[P1] Enviou para P{origem_destino} | Clock: {clock}")
        elif tipo == "recebimento":
            log(f"[P1] Recebeu de P{origem_destino} | Clock: {clock}")
        elif tipo == "interno":
            log(f"[P1] Evento interno | Clock: {clock}")

def servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", PORTA))
    s.listen()
    while True:
        conn, _ = s.accept()
        data = conn.recv(1024).decode()
        if data:
            if data.startswith("MARKER"):
                origem = int(data.split(":")[1])
                tratar_marcador(origem)
            else:
                origem, valor = data.split(":")
                recebido = int(valor)
                atualizar_relogio(recebido)
                registrar_evento("recebimento", origem[-1])
                if snapshot_iniciado and int(origem[-1]) not in marcadores_recebidos:
                    snapshot_mensagens_em_transito.append(data)
        conn.close()

def enviar_mensagem():
    global clock
    while True:
        time.sleep(5)
        for porta in VIZINHOS:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(("localhost", porta))
                    with lock:
                        clock += 1
                        mensagem = f"P1:{clock}"
                        s.sendall(mensagem.encode())
                        registrar_evento("envio", porta - 5000)
            except Exception as e:
                log(f"[P1] Erro ao enviar para porta {porta}: {e}")

def tratar_marcador(origem):
    global snapshot_iniciado, snapshot_estado_local
    if not snapshot_iniciado:
        snapshot_iniciado = True
        snapshot_estado_local = {
            "clock": clock,
            "contador_eventos": contador_eventos
        }
        log(f"[P1] *** Iniciou captura de estado ***: {snapshot_estado_local}")
        enviar_marcador()
    marcadores_recebidos.add(origem)
    if len(marcadores_recebidos) == len(VIZINHOS):
        log(f"[P1] *** Snapshot completo ***")
        log(f"[P1] Estado Local: {snapshot_estado_local}")
        log(f"[P1] Mensagens em trânsito: {snapshot_mensagens_em_transito}")

def enviar_marcador():
    for porta in VIZINHOS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("localhost", porta))
                marcador = f"MARKER:{PORTA}"
                s.sendall(marcador.encode())
                log(f"[P1] Enviou marcador para P{porta - 5000}")
        except Exception as e:
            log(f"[P1] Erro ao enviar marcador: {e}")

def evento_interno():
    while True:
        time.sleep(7)
        registrar_evento("interno")

def iniciar_snapshot_automatico():
    time.sleep(15)  # espera 15s
    tratar_marcador(PORTA)

if __name__ == "__main__":
    log("[P1] Iniciando processo com snapshot automático")
    threading.Thread(target=servidor, daemon=True).start()
    threading.Thread(target=enviar_mensagem, daemon=True).start()
    threading.Thread(target=evento_interno, daemon=True).start()
    iniciar_snapshot_automatico()
