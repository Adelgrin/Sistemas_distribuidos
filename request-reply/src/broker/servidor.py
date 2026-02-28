import zmq

tarefas = []

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://broker:5556")

def create(tarefa):
    tarefas.append(tarefa)
    # socket.send_string("tarefa adicionada")
    socket.send_string(listar())

def remove(tarefa):
    try:
        tarefas.remove(tarefa)
        socket.send_string("tarefa removida")
    except ValueError as e:
        socket.send_string(f"a tarefa {e} não existe")


def listar():
    payload = ""
    for i in tarefas:
        payload += (i + "\n")
    print(payload)
    # socket.send_string(payload)
    return payload

while True:
    message = socket.recv()
    # print(f"Mensagem recebida: {message}", flush=True)
    # socket.send_string("World")
    toprocess = str(message)
    toprocess.split()
    if toprocess[0].lower() == 'adiciona':
        create(toprocess[1])
    elif toprocess[0].lower() == 'remove':
        remove(toprocess[1])
    else:
        listar()
