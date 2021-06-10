from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    text=models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Entry(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    text=models.TextField()
    date_added=models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural='entries'
    
    def __str__(self):
        return f"{self.text[:50]}..."
    

class Video(models.Model):
    name=models.CharField(max_length=100)
    introduction=models.CharField(max_length=300)
    date_added=models.DateTimeField(auto_now_add=True)
    url=models.CharField(max_length=50)
    # url=models.FileField(upload_to='')

    owner_name=models.CharField(max_length=100)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.name