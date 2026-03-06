import zmq
from time import  sleep
from datetime import datetime

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.connect("tcp://proxy:5555")

while True:
    message = datetime.now().strftime("%H:%M:%S")
    print(f"Hora: {message}", flush=True)
    pub.send_string("hora {}".format(message))
    sleep(1)

pub.close()
context.close()
