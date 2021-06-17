from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateField

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
    class Meta:
        ordering=['-date_added','-id']
    # url=models.FileField(upload_to='')

    owner_name=models.CharField(max_length=100)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Comment(models.Model):
    content=models.TextField(help_text="Please Enter Your Comment...")
    date_added=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    video=models.ForeignKey(Video,on_delete=models.CASCADE)
    class Meta:
        ordering=['-date_added','-id']
    def __str__(self):
        return self.content

class CommentReply(models.Model):
    content=models.TextField(help_text="Please Enter Your Reply...")
    date_added=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,related_name='comment_owner',on_delete=models.CASCADE)
    parent_comment=models.ForeignKey(Comment, on_delete=models.CASCADE,blank=True, null=True)
    reply_to=models.ForeignKey(User, related_name='comment_reply_to',on_delete=models.RESTRICT,blank=True, null=True)
    class Meta:
        ordering=['-date_added','-id']
    def __str__(self):
        return self.content

class CommentInform(models.Model):
    date_added=models.DateTimeField(auto_now_add=True)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    read=models.BooleanField(default=False)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        ordering=['read','-date_added']

class CommentReplyInform(models.Model):
    date_added=models.DateTimeField(auto_now_add=True)
    comment_reply=models.ForeignKey(CommentReply,on_delete=models.CASCADE)
    read=models.BooleanField(default=False)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        ordering=['read','-date_added']

