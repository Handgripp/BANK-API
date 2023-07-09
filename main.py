from flask_apscheduler import APScheduler

from app import create_app, rabbitmq_config, check_credits
from multiprocessing import Process, Queue
from services.queue_service import mail_consumer


if __name__ == '__main__':
    app = create_app()
    queue = Queue()

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.add_job(id='check_credits', func=check_credits, args=[app], trigger='cron', hour=21, minute=0)
    scheduler.start()

    queue_consumer_process = Process(target=mail_consumer, args=(rabbitmq_config, queue))
    queue_consumer_process.start()

    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        queue_consumer_process.terminate()
        queue_consumer_process.join()
