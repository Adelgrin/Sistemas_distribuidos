import pika
from time import sleep
import uuid

reply = None

def callback(channel, method, properties, body):
    msg = body.decode("utf-8")
    global reply
    reply = body.decode("utf-8")

sleep(3)
conn_parameters = pika.ConnectionParameters(
        "rabbitmq",
        5672,
        "/",
        pika.PlainCredentials("user", "passwd"))
connection = pika.BlockingConnection(conn_parameters)
channel = connection.channel()
res = channel.queue_declare(queue="",exclusive=True)
callback_queue = res.method.queue
channel.basic_consume(
    queue=callback_queue,
    on_message_callback=callback,
    auto_ack=True
)
correlation_id = str(uuid.uuid4())

count = 0
while True:
    y = count+1
    channel.basic_publish(
        exchange="",
        routing_key="rpc_queue",
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=correlation_id
        ),
        body=f"{count} {y}"
    )
    while reply is None:
        connection.process_data_events(time_limit=None)

    print(f"Client: {count} + {y} = {reply}")
    count += 1
    sleep(1)

connection.close()
