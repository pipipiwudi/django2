from django import forms
from operations import models


class AddAskForm(forms.ModelForm):
    class Meta:
        model = models.UserAsk
        fields = ['name', 'mobile', 'course_name']