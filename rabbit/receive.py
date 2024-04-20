import pika

from config import RABBIT_MAIN_QUEUE, RABBIT_HOSTNAME


def receive_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOSTNAME))
    channel = connection.channel()

    channel.queue_declare(queue=RABBIT_MAIN_QUEUE)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue=RABBIT_MAIN_QUEUE, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()