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
                         exchange_type="direct")

count = 0
severities = ["info", "warning", "error"]
while True:
    severity = severities[count % len(severities)]
    msg = f"hello world {count} - {severity}"
    print(msg)
    channel.basic_publish(exchange="logs",
                          routing_key=severity,
                          body=msg)
    count += 1
    sleep(1)

connection.close()
