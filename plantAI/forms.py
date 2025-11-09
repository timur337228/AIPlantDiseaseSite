from django import forms
from django.contrib.auth import authenticate
from .models import PlantInfo

class PlantForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = PlantInfo
        fields = ("image", )