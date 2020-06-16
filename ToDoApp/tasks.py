from celery import shared_task
from django.core.mail import send_mail

@shared_task
def on_task_changed(id = None, completed = False):
    mail_title = 'Task status changed'
    mail_body = 'Task {id} has been marked as {status}'.format(id=id, status='completed' if completed else 'uncompleted')
    mail_sender = 'sender@example.com'
    mail_receivers = ['receiver@example.com']
    send_mail(mail_title, mail_body, mail_sender, mail_receivers)
    return None