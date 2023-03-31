from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse


STATUS = ((0, "Draft"), (1, "Published"))


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('blog_home')


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    body = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=255, default='trips')
    status = models.IntegerField(choices=STATUS, default=1)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def number_of_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('blog_home')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
