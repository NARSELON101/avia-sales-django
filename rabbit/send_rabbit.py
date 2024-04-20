import pika

from config import RABBIT_MAIN_QUEUE, RABBIT_HOSTNAME


def send_message_to_rabbit(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOSTNAME))
    channel = connection.channel()

    channel.queue_declare(queue=RABBIT_MAIN_QUEUE)

    channel.basic_publish(exchange='', routing_key=RABBIT_MAIN_QUEUE, body=message)
    print(" [x] Sent 'Hello World!'")
    connection.close()
