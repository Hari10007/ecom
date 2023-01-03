from django import forms
from order.models import Order, Refund

class OrderForm(forms.ModelForm):
    statuses =( 
        ('Confirmed','Confirmed'),
        ('Out For Shipping', 'Out For Shipping'),
        ('Delivered', 'Delivered'),
    )
    status = forms.ChoiceField(label="", choices = statuses)

    class Meta:
        model = Order
        fields = ['status']

class RefundForm(forms.ModelForm):

    class Meta:
        model = Refund
        fields = ['reason']