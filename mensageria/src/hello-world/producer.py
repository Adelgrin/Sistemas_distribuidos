import pika
from time import sleep

sleep(3)
conn_parameters = pika.ConnectionParameters(
        "rabbitmq",
        5672,
        "/",
        pika.PlainCredentials("user", "passwd"))
connection = pika.BlockingConnection(conn_parameters)
channel = connection.channel()
channel.queue_declare(queue="fila")

count = 0
while True:
    msg = f"hello world {count}"
    print(msg)
    channel.basic_publish(exchange="",
                          routing_key="fila",
                          body=msg)
    count += 1
    sleep(1)

connection.close()
