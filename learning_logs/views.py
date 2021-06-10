from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponse
from .models import Topic,Entry
from .forms  import TopicForm,EntryForm
from .models import Video
from .forms  import VideoForm,VideoInfoForm,SearchForm,VideoFileForm
from django.conf import settings
import os
# Create your views here.
def index(request):
    return render(request,'learning_logs/index.html')

@login_required
def videos(request):
    videos=Video.objects.filter(owner=request.user).order_by('date_added')
    context={'videos':videos}
    return render(request,'learning_logs/videos.html',context)
# @login_required
# def new_video(request):
#     if request.method!='POST':
#         form=VideoForm()
#     else:
#         form=VideoForm(data=request.POST)
#         if form.is_valid():
#             new_video=form.save(commit=False)
#             new_video.owner=request.user
#             new_video.owner_name=str(request.user)
#             new_video.save()
#             return redirect('learning_logs:videos')
#     context={'form':form}
#     return render(request,'learning_logs/new_video.html',context)

@login_required
def new_video(request):
    if request.method!='POST':
        form=VideoFileForm()
    else:
        form=VideoFileForm(data=request.POST,files=request.FILES)
        form_video_info=VideoInfoForm(data=request.POST)
        f=request.FILES.get('video_file',None)
        if form.is_valid() and f and f.name.split('.',1)[1]=='mp4':
            if Video.objects.filter(name=request.POST['name'],owner=request.user).exists():
                return render(request,'learning_logs/name_repeat_load.html')
            filepath = os.path.join(settings.MEDIA_ROOT, str(request.user),request.POST['name']+'.mp4')
            dirpath=os.path.join(settings.MEDIA_ROOT, str(request.user))
            if not os.path.isdir(dirpath):
                os.mkdir(dirpath)
            with open(filepath, 'wb') as fp:
                for info in f.chunks():
                    fp.write(info)
                fp.close()
            new_video=form_video_info.save(commit=False)
            new_video.owner=request.user
            new_video.owner_name=str(request.user)
            new_video.url=os.path.join(str(request.user),request.POST['name']+'.mp4')
            new_video.save()
            return render(request,'learning_logs/success_load.html')
        else:
            return render(request,'learning_logs/invalid_load.html')
            
    context={'form':form}
    return render(request,'learning_logs/new_video.html',context)

@login_required
def edit_video_info(request,video_id):
    video = Video.objects.get(id=video_id)

    if video.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = VideoInfoForm(instance=video)
    else:
        form = VideoInfoForm(instance=video,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:videos')
    context={'video':video,'form':form}
    return render(request,'learning_logs/edit_video_info.html',context)

@login_required
def delete_video(request,video_id):
    video_delete=Video.objects.get(id=video_id)
    delete_path=os.path.join(settings.MEDIA_ROOT,video_delete.owner_name,video_delete.name+'.mp4')
    os.remove(delete_path)
    Video.objects.filter(id=video_id).delete()
    return redirect('learning_logs:videos')
    
@login_required
def search(request):
    if request.method!='POST':
        form=SearchForm()
    else:
        form=SearchForm(data=request.POST)
        if form.is_valid():
            if request.POST['chioce']=='1':
                videos=Video.objects.filter(name__icontains=request.POST['key'])
            else:
                videos=Video.objects.filter(owner_name__icontains=request.POST['key'])
            context={'form':form,'videos':videos}
            return render(request,'learning_logs/search.html',context)
    context={'form':form}
    return render(request,'learning_logs/search.html',context)
    

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request,'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context={'topic':topic,'entries':entries}
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    
    context = {'form':form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic',topic_id=topic_id)
    context={'form':form,'topic':topic}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)
    context={'entry':entry,'form':form,'topic':topic}
    return render(request,'learning_logs/edit_entry.html',context)
