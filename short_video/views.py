from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404,HttpResponse,JsonResponse
from .models import Topic,Entry
from .forms  import CommentReplyForm, TopicForm,EntryForm
from .models import Video,Comment,CommentReply,CommentInform,CommentReplyInform
from .forms  import VideoForm,VideoInfoForm,SearchForm,VideoFileForm,CommentForm,CommentReplyForm,CommentInformForm,CommentReplyInformForm
from django.conf import settings
import os
# Create your views here.
def index(request):
    return render(request,'short_video/index.html')

@login_required
def videos(request):
    videos=Video.objects.filter(owner=request.user).order_by('-date_added')
    form_comment_reply=CommentReplyForm()
    form_comment=CommentForm()
    context={'videos':videos,'form_comment':form_comment,'form_comment_reply':form_comment_reply}
    return render(request,'short_video/videos.html',context)
@login_required
def video(request,video_id):
    video=Video.objects.get(id=video_id)
    form_comment_reply=CommentReplyForm()
    form_comment=CommentForm()
    context={'video':video,'form_comment':form_comment,'form_comment_reply':form_comment_reply}
    return render(request,'short_video/video.html',context)

@login_required
def inform(request):
    form_comment_reply=CommentReplyForm()
    unread_comment_inform_cnt=len(CommentInform.objects.filter(owner=request.user,read=False))
    unread_comment_reply_inform_cnt=len(CommentReplyInform.objects.filter(owner=request.user,read=False))
    context={
        'unread_comment_inform_cnt':unread_comment_inform_cnt,
        'unread_comment_reply_inform_cnt':unread_comment_reply_inform_cnt,
        'form_comment_reply':form_comment_reply
        }
    return render(request,'short_video/inform.html',context)

@login_required
def read_comment_inform(request,comment_inform_id):
    comment_inform=CommentInform.objects.get(id=comment_inform_id)
    if comment_inform.owner!=request.user:
        raise Http404
    form=CommentInformForm(data={'read':True},instance=comment_inform)
    form.save()
    return redirect('short_video:inform')

@login_required
def read_comment_inform_all(request):
    comment_informs=CommentInform.objects.filter(owner=request.user,read=False)
    for comment_inform in comment_informs:
        form=CommentInformForm(data={'read':True},instance=comment_inform)
        form.save()
    return redirect('short_video:inform')

@login_required
def delete_comment_inform(request,comment_inform_id):
    comment_inform_delete=CommentInform.objects.get(id=comment_inform_id)
    if comment_inform_delete.owner!=request.user:
        raise Http404
    comment_inform_delete.delete()
    return redirect('short_video:inform')

@login_required
def delete_comment_inform_all(request):
    CommentInform.objects.filter(owner=request.user).delete()
    return redirect('short_video:inform')

@login_required
def read_comment_reply_inform(request,comment_reply_inform_id):
    comment_reply_inform=CommentReplyInform.objects.get(id=comment_reply_inform_id)
    if comment_reply_inform.owner!=request.user:
        raise Http404
    form=CommentReplyInformForm(data={'read':True},instance=comment_reply_inform)
    form.save()
    return redirect('short_video:inform')

@login_required
def read_comment_reply_inform_all(request):
    comment_reply_informs=CommentReplyInform.objects.filter(owner=request.user,read=False)
    for comment_reply_inform in comment_reply_informs:
        form=CommentReplyInformForm(data={'read':True},instance=comment_reply_inform)
        form.save()
    return redirect('short_video:inform')

@login_required
def delete_comment_reply_inform(request,comment_reply_inform_id):
    comment_reply_inform_delete=CommentReplyInform.objects.get(id=comment_reply_inform_id)
    if comment_reply_inform_delete.owner!=request.user:
        raise Http404
    comment_reply_inform_delete.delete()
    return redirect('short_video:inform')

@login_required
def delete_comment_reply_inform_all(request):
    CommentReplyInform.objects.filter(owner=request.user).delete()
    return redirect('short_video:inform')

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
                return render(request,'short_video/name_repeat_load.html')
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
            return render(request,'short_video/success_load.html')
        else:
            return render(request,'short_video/invalid_load.html')
            
    context={'form':form}
    return render(request,'short_video/new_video.html',context)

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
            return redirect('short_video:videos')
    context={'video':video,'form':form}
    return render(request,'short_video/edit_video_info.html',context)

@login_required
def delete_video(request,video_id):
    video_delete=Video.objects.get(id=video_id)
    if video_delete.owner != request.user:
        raise Http404
    delete_path=os.path.join(settings.MEDIA_ROOT,video_delete.owner_name,video_delete.name+'.mp4')
    os.remove(delete_path)
    Video.objects.filter(id=video_id).delete()
    return redirect('short_video:videos')
    
@login_required
def search(request):
    form_comment=CommentForm()
    form_comment_reply=CommentReplyForm()
    if request.method!='POST':
        form=SearchForm()
    else:
        form=SearchForm(data=request.POST)
        if form.is_valid():
            if request.POST['chioce']=='1':
                videos=Video.objects.filter(name__icontains=request.POST['key'])
            else:
                videos=Video.objects.filter(owner_name__icontains=request.POST['key'])
            context={'form':form,'videos':videos,'form_comment_reply':form_comment_reply,'form_comment':form_comment}
            return render(request,'short_video/search.html',context)
    context={'form':form,'form_comment_reply':form_comment_reply,'form_comment':form_comment}
    return render(request,'short_video/search.html',context)
    



@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request,'short_video/topics.html',context)

@login_required
def topic(request,topic_id):
    
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context={'topic':topic,'entries':entries}
    return render(request,'short_video/topic.html',context)

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
            return redirect('short_video:topics')
    
    context = {'form':form}
    return render(request,'short_video/new_topic.html',context)

@login_required
def comment_video(request,video_id):
    video=Video.objects.get(id=video_id)
    if request.method=='POST':
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.owner=request.user
            new_comment.video=video
            new_comment.save()

            if request.user!=video.owner:
                new_comment_id=new_comment.id
                form_inform=CommentInformForm(data={'read':False})
                new_comment_inform=form_inform.save(commit=False)
                new_comment_inform.owner=video.owner
                new_comment_inform.comment=Comment.objects.get(id=new_comment_id)
                new_comment_inform.save()
            return redirect('short_video:video',video_id)
    else:
        raise Http404

@login_required
def reply_comment(request,comment_id,reply_to_user_id):
    comment=Comment.objects.get(id=comment_id)
    if request.method=='POST':
        form=CommentReplyForm(data=request.POST)
        if form.is_valid():
            new_comment_reply=form.save(commit=False)
            new_comment_reply.owner=request.user
            new_comment_reply.parent_comment=comment
            if reply_to_user_id>0:
                new_comment_reply.reply_to=User.objects.get(id=reply_to_user_id)
            new_comment_reply.save()

            if not((reply_to_user_id==0 and comment.owner==request.user) or (reply_to_user_id>0 and reply_to_user_id==request.user.id) ):
                new_comment_reply_id=new_comment_reply.id
                form_inform=CommentReplyInformForm(data={'read':False})
                new_comment_reply_inform=form_inform.save(commit=False)
                new_comment_reply_inform.comment_reply=CommentReply.objects.get(id=new_comment_reply_id)
                if reply_to_user_id==0:
                    new_comment_reply_inform.owner=comment.owner
                else:
                    new_comment_reply_inform.owner=User.objects.get(id=reply_to_user_id)
                new_comment_reply_inform.save()
            return redirect('short_video:video',comment.video.id)
    else:
        raise Http404
@login_required
def delete_comment(request,comment_id):
    comment_delete=Comment.objects.get(id=comment_id)
    id=comment_delete.video.id
    if comment_delete.owner!=request.user:
        raise Http404
    Comment.objects.filter(id=comment_id).delete()
    return redirect('short_video:video',id)
@login_required
def delete_comment_reply(request,comment_reply_id):
    comment_reply_delete=CommentReply.objects.get(id=comment_reply_id)
    id=comment_reply_delete.video.id
    if comment_reply_delete.owner!=request.user:
        raise Http404
    CommentReply.objects.filter(id=comment_reply_id).delete()
    return redirect('short_video:video',id)


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
            return redirect('short_video:topic',topic_id=topic_id)
    context={'form':form,'topic':topic}
    return render(request,'short_video/new_entry.html',context)

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
            return redirect('short_video:topic',topic_id=topic.id)
    context={'entry':entry,'form':form,'topic':topic}
    return render(request,'short_video/edit_entry.html',context)
