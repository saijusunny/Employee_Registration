from .models import Employee
from django import forms
from django.contrib.auth.models import User, Group


class EmployeeForm(forms.ModelForm):
    # user=forms.ModelChoiceField(queryset=Group.objects.all())
    class Meta:
        model = Employee
        fields = ['name','pic','mobile','email','salary']

