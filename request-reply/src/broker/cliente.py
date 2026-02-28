import zmq
from time import sleep
import random

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://broker:5555")

acoes = ["adiciona", "remove"]
tarefas = ["arrumar_cama","fazer_projeto","bom_dia","cleitin","TCC","enfim"]


while True:
    # print(f"Mensagem {i}:", end=" ", flush=True)
    # socket.send(b"Hello")
    # mensagem = socket.recv()
    # print(f"{mensagem}")
    oqfazer = f"{random.sample(acoes,1)[0]} {random.sample(tarefas,1)[0]}"
    # print(oqfazer)
    socket.send_string(oqfazer)
    mensagem = socket.recv()
    print(f"{mensagem}")
    sleep(0.5)

