from .models import Comment, Post, Category
from django import forms
from django_summernote.widgets import SummernoteWidget

choices = Category.objects.all().values_list('name', 'name')

choice_list = []

for item in choices:
    choice_list.append(item)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'category', 'body', 'snippet', 'featured_image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'user', 'type': 'hidden'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'body': SummernoteWidget(),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'featured_image', 'body', 'snippet')

        widgets = {
            'body': SummernoteWidget(),
            # 'feature_image': forms.ImageField(),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body') 
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
