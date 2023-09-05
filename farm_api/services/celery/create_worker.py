"""Create a celery worker."""

from celery import Celery


def make_celery(app_name: str = __name__) -> Celery:
    """Create a celery worker.

    :param app_name: name of the app

    :return: celery worker
    """
    backend = "redis://llama2_redis_1:6379/0"
    return Celery(app_name, backend=backend, broker=backend)
