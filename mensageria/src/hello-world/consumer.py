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

def callback(ch, method, properties, body):
    msg = body.decode("utf-8")
    print(f"Recebido: {msg}")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(queue="fila",
                      on_message_callback=callback)

channel.start_consuming()
