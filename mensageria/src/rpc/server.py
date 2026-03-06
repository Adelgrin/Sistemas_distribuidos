import pika
from time import sleep

def soma(x, y):
    return x + y

def callback(ch, method, properties, body):
    x, y = [int(v) for v in body.decode("utf-8").split()]
    res = soma(x, y)
    print(f"{x} + {y} = {res}")
    ch.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id = properties.correlation_id ),
        body=str(res)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

sleep(3)
conn_parameters = pika.ConnectionParameters(
        "rabbitmq",
        5672,
        "/",
        pika.PlainCredentials("user", "passwd"))
connection = pika.BlockingConnection(conn_parameters)
channel = connection.channel()
channel.queue_declare(queue="rpc_queue")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="rpc_queue",
                      on_message_callback=callback)
channel.start_consuming()
