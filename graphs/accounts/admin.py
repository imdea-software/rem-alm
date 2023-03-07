from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name','email')
    list_filter = ('is_staff', 'is_superuser','email')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class UserProfile(admin.ModelAdmin):
    list_display = ('user', 'view')
    list_filter = ('user','view')
    actions = ['deactivate','delete']

admin.site.register(Profile, UserProfile)