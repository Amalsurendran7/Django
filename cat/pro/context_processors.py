from .models import *

def menu_links(request):
    links = category.objects.all()
    return dict(links=links)

def filter_links(request):
    k=produc.objects.all()
    return dict(k=k)    
