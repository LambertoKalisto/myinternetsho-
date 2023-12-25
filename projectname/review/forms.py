from .models import Reviews
from django.forms import ModelForm, TextInput, DateTimeInput, NumberInput, Textarea


class ReviewsForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ['name', 'full_text', 'rate', 'date']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ім'я користувача",
            }),
            "full_text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Текст відгуку",
            }),
            "rate": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Оцінка",
                'min': 1,
                'max': 5
            }),
            "date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': "Дата публікації",
            })
        }