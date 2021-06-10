from django.urls import path,include,re_path

from django.conf import settings
from django.views.static import serve


from . import views

app_name = 'learning_logs'
urlpatterns = [
    path('',views.index,name='index'),
    path('videos/',views.videos,name='videos'),
    path('new_video/',views.new_video,name='new_video'),
    path('edit_video_info/<int:video_id>/',views.edit_video_info,name='edit_video_info'),
    path('delete_video/<int:video_id>/',views.delete_video,name='delete_video'),
    path('search/',views.search,name='search'),

    path('topics/',views.topics,name='topics'),
    path('topics/<int:topic_id>/',views.topic,name='topic'),
    path('new_topic/',views.new_topic,name='new_topic'),
    path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),
    path('edit_entry/<int:entry_id>/',views.edit_entry,name='edit_entry'),

    re_path("media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
