import django_filters

from orders.models import *
from .models import *


class productFilter(django_filters.FilterSet):
    class Meta:
        model=produc
        fields=['name']



class orderFilter(django_filters.FilterSet):
    class Meta:
        model=OrderProduct
        fields=['status','product','order','quantity']


       

