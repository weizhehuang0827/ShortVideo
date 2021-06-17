from django.contrib import admin

# Register your models here.
from .models import Topic,Entry,Video,Comment,CommentReply

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(CommentReply)