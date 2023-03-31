from .models import Comment, Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'body')


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
