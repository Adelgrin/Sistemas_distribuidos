import zmq
from time import sleep

context = zmq.Context()
sub = context.socket(zmq.SUB)
sub.setsockopt_string(zmq.SUBSCRIBE, "hora")
sub.setsockopt_string(zmq.SUBSCRIBE, "numero")
sub.connect("tcp://proxy:5556")

while True:
    message = sub.recv_string()
    print(f"M: {message}", flush=True)

sub.close()
context.close()
