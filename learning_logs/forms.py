from django import forms
from django.forms import fields, widgets

from .models import Topic,Entry
from .models import Video

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text':' '}
        widgets = {'text':forms.Textarea(attrs={'col':80})}

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name','introduction','url']
        labels = {'name':'name:','introduction':'introduction:','url':'url:'}
        widgets = {'introduction':forms.Textarea(attrs={'col':80})}

class VideoInfoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name','introduction']
        labels = {'name':'name:','introduction':'introduction:'}
        widgets = {'introduction':forms.Textarea(attrs={'col':80})}
CHOICES=(('1','NAME'),('2','OWNER'))
class SearchForm(forms.Form):
    chioce=forms.CharField(label='Chioce',widget=forms.widgets.Select(choices=CHOICES))
    key=forms.CharField(label='Key')
    
class VideoFileForm(forms.Form):
    name=forms.CharField(label='name')
    introduction=forms.CharField(label='introduction',widget=forms.widgets.Textarea(attrs={'col':80}))
    video_file=forms.FileField(label='video_file')