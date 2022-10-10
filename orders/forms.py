from django import forms
from .models import Order, OrderProduct



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [ 'address_line_2','payment_method']

class OPForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = '__all__'







