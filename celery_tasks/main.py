from celery import Celery
from celery.utils.log import get_task_logger
import os

# 读取django项目的配置
# os.environ["DJANGO_SETTINGS_MODULE"] = "dailyfresh.settings"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
app = Celery("main")
app.config_from_object("celery_tasks.config")

app.autodiscover_tasks([
    "celery_tasks.email"
])

# logger = get_task_logger("dailyfresh_celery")
# logger.info("Refresh task start and refresh success")