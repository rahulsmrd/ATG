from django.db import models
from django.contrib.auth.models import User as mainUser
from django.utils import timezone

# Create your models here.
class post(models.Model):
    user=models.ForeignKey(mainUser,related_name='posts',on_delete=models.CASCADE)
    title=models.CharField(max_length=1000)
    image=models.FileField(upload_to='post_images')
    category=models.CharField(max_length=500)
    summary=models.TextField(blank=False, max_length=1000)
    content=models.TextField(blank=False, max_length=2000)
    published=models.BooleanField(default=False)
    published_date=models.DateField(null=True,blank=True)

    def publish(self):
        self.published = True
        self.published_date = timezone.now()
        self.save()
        return
    
    def unpublish(self):
        self.published = False
        self.published_date = None
        self.save()
        return
    
    def publishedcount(self):
        return self.published.count()