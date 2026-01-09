from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed'] # Added due_date
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 3}),
            # This 'type': 'date' triggers the browser's built-in calendar
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), 
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }