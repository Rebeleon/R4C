from django.http import HttpResponse
from django.db.models import Count
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from openpyxl import Workbook
from robots.models import Robot
from orders.models import Order


EMAIL_HOST_USER = ''


def download_summary_logic():
    current_date = datetime.now().date()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    workbook = Workbook()
    unique_models = Robot.objects.filter(created__gte=start_of_week).values('model').distinct()
    for model in unique_models:
        model_name = model['model']
        sheet = workbook.create_sheet(title=model_name)
        sheet.append(['Модель', 'Версия', 'Количество за неделю'])
        unique_versions = (Robot.objects.filter(model=model_name, created__gte=start_of_week).values('model', 'version')
                           .annotate(total_count=Count('id')))
        for version in unique_versions:
            sheet.append([version['model'], version['version'], version['total_count']])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="summary.xlsx"'
    workbook.save(response)
    return response


def send_email(recipient_list, model, version):
    email_from = EMAIL_HOST_USER
    recipient_list = recipient_list
    subject = ''
    message = f'''
            Добрый день!
            Недавно вы интересовались нашим роботом модели {model}, версии {version}. 
            Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами
            '''
    send_mail(subject, message, email_from, recipient_list)


@receiver(post_save, sender=Robot)
def handle_save(sender, instance, created, **kwargs):
    serial = instance.model + '-' + instance.version
    orders = Order.objects.filter(robot_serial=serial)
    if orders:
        recipient_list = [order.customer.email for order in orders]
        send_email(recipient_list, instance.model, instance.version)
