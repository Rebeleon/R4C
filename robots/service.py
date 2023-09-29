from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime, timedelta
from openpyxl import Workbook
from robots.models import Robot


def download_summary_logic(request):
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
