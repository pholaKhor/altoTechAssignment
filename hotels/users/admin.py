from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from .models import CustomUser, UserType, PermissionType, UserPermission

# Register your models here.   
class EditUser(admin.ModelAdmin):
    user = models.ForeignKey(User, unique=True, related_name='profile', on_delete=models.CASCADE)
    user_type = models.IntegerField(choices=UserType.choices, default=UserType.GUEST)

class EditUserPermission(admin.ModelAdmin):
    user_type = models.IntegerField(choices=UserType.choices)
    permission_type = models.IntegerField(choices=PermissionType.choices)


admin.site.register(CustomUser, EditUser)
admin.site.register(UserPermission, EditUserPermission)