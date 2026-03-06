import zmq
from time import time, sleep
import random

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.connect("tcp://proxy:5555")

while True:
    message = random.randint(1,6)
    print(f"Numero: {message}", flush=True)
    pub.send_string("numero {}".format(message))
    sleep(1)

pub.close()
context.close()
