from django import forms
from .models import  Product, Category, ProductImage
from django.forms import ClearableFileInput
from account.models import User
import datetime


class ProductForm(forms.ModelForm):
    slug = forms.SlugField(widget=forms.TextInput(attrs={'class': 'form-input'}),required=False)
    main_image = forms.FileField()

    class Meta:
        model = Product
        fields = ['name','category','slug','main_image','description','quantity','price','available']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
        widgets = {
            'image': ClearableFileInput(attrs={'multiple': True}),
        }

class CategoryForm(forms.ModelForm):
    slug = forms.SlugField(widget=forms.TextInput(attrs={'class': 'form-input'}),required=False)

    class Meta:
        model = Category
        fields = ['name','parent','slug','image','description']
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            message = "Password doesn't match!"
            self.add_error('confirm_password', message)

    def _init_(self, *args, **kwargs):
        super(UserForm, self)._init_(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'


class DateForm(forms.Form):
    year_dropdown = []
    year_dropdown.insert(0, ('', '----'))

    for y in range(2015, (datetime.datetime.now().year + 5)):
        year_dropdown.append((y, y))

    month_dropdown = ( 
        ('', '----'),
        ('1','January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    )
    year = forms.ChoiceField(choices=year_dropdown, required=False)
    month = forms.ChoiceField(choices=month_dropdown, required=False)

    class Meta:
        fields = ['year', 'month']
