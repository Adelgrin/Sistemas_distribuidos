import zmq
from time import sleep
import random

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://broker:5555")

acoes = ["adiciona", "remove"]
tarefas = ["arrumar_cama", "fazer_projeto", "bom_dia", "cleitin", "TCC", "enfim"]

try:
    while True:
        oqfazer = f"{random.choice(acoes)} {random.choice(tarefas)}"
        socket.send_string(oqfazer)
        resposta = socket.recv_string()
        print(resposta)
        sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    socket.close()
    context.term()


