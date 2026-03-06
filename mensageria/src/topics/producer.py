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
                         exchange_type="topic")

count = 0
severities = ["info", "warning", "error"]
origins = ["sever1", "server2"]
while True:
    severity = severities[count % len(severities)]
    origin = origins[count % len(origins)]
    routing_key= f"{origin}.{severity}"
    msg = f"hello world {count} - {routing_key}"
    print(msg)
    channel.basic_publish(exchange="logs",
                          routing_key=routing_key,
                          body=msg)
    count += 1
    sleep(1)

connection.close()
