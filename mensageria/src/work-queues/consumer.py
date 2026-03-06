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
channel.queue_declare(queue="work_queue")

def callback(ch, method, properties, body):
    msg = body.decode("utf-8")
    print(f"Deve executar algo por {msg} segundos")
    tempo = int(msg)
    sleep(tempo)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(queue="work_queue",
                      on_message_callback=callback)

channel.start_consuming()
