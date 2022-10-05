
from django import forms

from orders.models import *
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model=produc
        fields=['name','price','description','img','img2','img3','img4','cate_id','stock']

class CustomerForm(forms.ModelForm):
    class Meta:
        model=customer
        fields='__all__'

class OForm(forms.ModelForm):
    class Meta:
        model=OrderProduct
        fields=['status']


class AddressForm(forms.ModelForm):
    class Meta:
        model=Address     
        fields='__all__' 



class BannerForm(forms.ModelForm):
      class Meta:
        model=banner
        fields='__all__'
       


 
class categoryForm(forms.ModelForm):
    class Meta:
        model=category
        fields='__all__'       


