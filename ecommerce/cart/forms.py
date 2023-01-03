from django import forms
from account.models import  Address

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['address','city','country','postal_code']