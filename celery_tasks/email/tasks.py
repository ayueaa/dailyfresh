from django.conf import settings
from django.core.mail import send_mail
from celery_tasks.main import app
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@app.task(bind=True, name="send_sms", retry_backoff=3)
def send_sms(self, to_email, verify_url):
    subject = "天天生鲜邮箱验证"
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用天天生鲜。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    try:
        send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)
    except Exception as e:
        self.retry(exc=e, max_retries=3)
