from app import create_app, rabbitmq_config
from multiprocessing import Process, Queue
from services.queue_service import mail_consumer


if __name__ == '__main__':
    app = create_app()
    queue = Queue()

    queue_consumer_process = Process(target=mail_consumer, args=(rabbitmq_config, queue))
    queue_consumer_process.start()

    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        queue_consumer_process.terminate()
        queue_consumer_process.join()
