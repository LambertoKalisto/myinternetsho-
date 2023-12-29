from .models import Order
from django.forms import ModelForm, TextInput, NumberInput, HiddenInput
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['Name', 'SurName', 'Adress', 'PhoneNumber']

        widgets = {
            "Name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ім'я",
            }),
            "SurName": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Прізвище",
            }),
            "Adress": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Адресса",
            }),
            "PhoneNumber": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Номер телефону",
                'oninput': "this.value = this.value.slice(0, 10)",
            }),
        }