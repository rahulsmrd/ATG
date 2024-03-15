from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User as mainUser

# Create your models here.
class User(auth.models.User,auth.models.PermissionsMixin):
    def __str__(self):
        return "@{}".format(self.username)
    
    def is_doctor(self):
        prof=profile.objects.get(user=self.username)
        print(prof.is_doctor)
        return prof.is_doctor
    
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
        return str(self.user)

class contact_model(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=200)
    description=models.TextField()

    def __str__(self) -> str:
        return self.name
    

class appointment_model(models.Model):
    user = models.ForeignKey(mainUser, related_name="appointments",on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=200)
    doctor_email = models.EmailField(max_length=500)
    speciality=models.CharField(max_length=200)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True,null=True)
    confirm=models.BooleanField(default=False)
    event_id=models.CharField(max_length=200,blank=True,null=True)

    def confirm_appointment(self):
        self.confirm=True
        self.save()
        return
    def enter_event_id(self,id):
        self.event_id=id
        self.save()
        return
    def enter_end_time(self,end_time):
        self.end_time=end_time
        self.save()
        return