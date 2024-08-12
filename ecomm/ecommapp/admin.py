from django.contrib import admin
from ecommapp.models import product
# Register your models here.
class productadmin(admin.ModelAdmin):
    list_display=["id","name","price","pdetails","category","is_active"]
    list_filter=["category","is_active"]
admin.site.register(product,productadmin)