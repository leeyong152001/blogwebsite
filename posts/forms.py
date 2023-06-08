from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, Comment

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        body = TinyMCE
        fields = ('title', 'slug','intro', 'body', 'categories', 
        'image' , 'status')