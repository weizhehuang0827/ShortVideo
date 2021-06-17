from os import name
from django.urls import path,include,re_path

from django.conf import settings
from django.views.static import serve


from . import views

app_name = 'short_video'
urlpatterns = [
    path('',views.index,name='index'),
    path('videos/',views.videos,name='videos'),
    path('new_video/',views.new_video,name='new_video'),
    path('edit_video_info/<int:video_id>/',views.edit_video_info,name='edit_video_info'),
    path('delete_video/<int:video_id>/',views.delete_video,name='delete_video'),
    path('search/',views.search,name='search'),
    path('comment_video/<int:video_id>/',views.comment_video,name='comment_video'),
    path('reply_comment/<int:comment_id>/<int:reply_to_user_id>/',views.reply_comment,name='reply_comment'),
    path('delete_comment/<int:comment_id>/',views.delete_comment,name='delete_comment'),
    path('delete_comment_reply/<int:comment_reply_id>/',views.delete_comment_reply,name='delete_comment_reply'),
    path('video/<int:video_id>/',views.video,name='video'),
    path('inform/',views.inform,name='inform'),
    path('read_comment_inform/<int:comment_inform_id>/',views.read_comment_inform,name='read_comment_inform'),
    path('read_comment_reply_inform/<int:comment_reply_inform_id>/',views.read_comment_reply_inform,name='read_comment_reply_inform'),
    path('read_comment_inform_all/',views.read_comment_inform_all,name='read_comment_inform_all'),
    path('read_comment_reply_inform_all/',views.read_comment_reply_inform_all,name='read_comment_reply_inform_all'),
    path('delete_comment_inform/<int:comment_inform_id>/',views.delete_comment_inform,name='delete_comment_inform'),
    path('delete_comment_reply_inform/<int:comment_reply_inform_id>/',views.delete_comment_reply_inform,name='delete_comment_reply_inform'),
    path('delete_comment_inform_all/',views.delete_comment_inform_all,name='delete_comment_inform_all'),
    path('delete_comment_reply_inform_all/',views.delete_comment_reply_inform_all,name='delete_comment_reply_inform_all'),

    path('topics/',views.topics,name='topics'),
    path('topics/<int:topic_id>/',views.topic,name='topic'),
    path('new_topic/',views.new_topic,name='new_topic'),
    path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),
    path('edit_entry/<int:entry_id>/',views.edit_entry,name='edit_entry'),

    re_path("media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
