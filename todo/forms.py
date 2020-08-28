from django.forms import ModelForm
from .models import Todo


class Todo_form(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'important']
