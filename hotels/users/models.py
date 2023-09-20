from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserType(models.IntegerChoices):
        ADMIN = 0
        MAID_SUPERVISOR = 1
        SUPERVISOR = 2
        GUEST = 3 

class PermissionType(models.IntegerChoices):
        CREATE_WORK_ODER_CLEANING = 0
        CREATE_WORK_ODER_MAID_REQ = 1
        CREATE_WORK_ODER_TECHNICIAN_REQ = 2
        CREATE_WORK_ODER_AMENITY_REQ = 3   

class CustomUser(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, primary_key=True)
    user_type = models.IntegerField(choices=UserType.choices, default=UserType.GUEST)
    
class UserPermission(models.Model):
    user_type = models.IntegerField(choices=UserType.choices)
    permission_type = models.IntegerField(choices=PermissionType.choices)
    class Meta:
        unique_together = (("user_type", "permission_type"),)