from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User as mainUser

# Create your models here.
class User(auth.models.User,auth.models.PermissionsMixin):
    def __str__(self):
        return "@{}".format(self.username)
    
class profile(models.Model):
    user=models.OneToOneField(mainUser,related_name="profile", on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    picture= models.FileField(blank=True, null=True,upload_to='profile')
    address=models.CharField(max_length=500)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pin=models.PositiveIntegerField()
    is_doctor=models.BooleanField(default=False)
    doc_id=models.PositiveIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.user

class contact_model(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=200)
    description=models.TextField()

    def __str__(self) -> str:
        return self.name