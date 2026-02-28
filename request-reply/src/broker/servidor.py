import zmq

tarefas = []

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://broker:5556")

def create(tarefa):
    tarefas.append(tarefa)
    return "tarefa adicionada\n" + listar()

def remove(tarefa):
    try:
        tarefas.remove(tarefa)
        return "tarefa removida\n" + listar()
    except ValueError:
        return f"a tarefa {tarefa} não existe"


def listar():
    payload = ""
    for i in tarefas:
        payload += (i + "\n")
    print(payload)
    return payload

while True:
    message = socket.recv_string()
    parts = message.split()
    cmd = parts[0].lower() if parts else ""
    arg = parts[1] if len(parts) > 1 else None

    if cmd == 'adiciona' and arg:
        response = create(arg)
    elif cmd == 'remove' and arg:
        response = remove(arg)
    else:
        response = listar()

    socket.send_string(response)

