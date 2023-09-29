from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from robots.forms import RobotForm
from robots.service import download_summary_logic


@csrf_exempt
def create_robot(request):
    data = json.loads(request.body)
    form = RobotForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        errors = form.errors.as_json()
        return JsonResponse({'status': 'error', 'errors': errors})


def download_summary(request):
    return download_summary_logic()
