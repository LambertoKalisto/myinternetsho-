from .models import Order, Cart
from django.forms import ModelForm, TextInput, NumberInput, HiddenInput
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms

class OrderForm(ModelForm):
    products = forms.ModelMultipleChoiceField(queryset=Cart.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Order
        fields = ['name', 'surname', 'adress', 'phonenumber', 'products']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ім'я",
            }),
            "surname": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Прізвище",
            }),
            "adress": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Адресса",
            }),
            "phonenumber": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Номер телефону",
            }),
        }