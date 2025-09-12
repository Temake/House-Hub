from django.contrib import admin

# Register your models here.
from .models import house
class HouseAdmin(admin.ModelAdmin):
    readonly_fields=['id','created_on']
admin.site.register(house,HouseAdmin)