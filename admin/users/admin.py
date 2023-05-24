from django.contrib import admin
from .models import MyUser

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email','first_name','last_name',)
admin.site.register(MyUser, UserAdmin)

