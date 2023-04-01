from .models import Comment, Post, Category
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

choices = Category.objects.all().values_list('name', 'name')

choice_list = []

for item in choices:
    choice_list.append(item)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'author', 'category', 'body')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'user', 'type': 'hidden'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'body': SummernoteWidget()
        }


class EditForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body',)

        widgets = {
            'body': SummernoteWidget()

        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body': SummernoteWidget()
        }
