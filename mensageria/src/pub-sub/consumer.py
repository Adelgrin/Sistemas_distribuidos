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

channel.exchange_declare(exchange="logs",
                         exchange_type="fanout")

result = channel.queue_declare(queue="",
                               exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange="logs",
                   queue=queue_name)

def callback(ch, method, properties, body):
    msg = body.decode("utf-8")
    print(f"Recebido: {msg}")

channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)

channel.start_consuming()
