from django.contrib import admin

# Register your models here.
from .models import Profile

#class Admin(admin.ModelAdmin):
    #readonly_fields=['id',]
    


admin.site.register(Profile)