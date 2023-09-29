from django import forms
from robots.models import Robot


class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['model', 'version', 'created']
        widgets = {
            'created': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
