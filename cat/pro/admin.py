from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(customer)
admin.site.register(Address)
admin.site.register(Wallet)

admin.site.register(banner)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

admin.site.register(category, CategoryAdmin)

class fil(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('price',)}
    list_display = ('price', 'slug')


admin.site.register(produc)

