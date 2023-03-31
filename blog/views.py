from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Post, Category
from .forms import CommentForm, EditForm, PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class HomeView(ListView):
    model = Post
    template_name = 'post/index.html'
    ordering = ['-created_on']


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    return render(request, 'post/categories.html', {'cats': cats.title(), 'category_posts': category_posts})


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/add_post.html'


class AddCategoryView(CreateView):
    model = Category
    template_name = 'post/add_category.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'post/update_post.html'


class DeletePostView(DeleteView):
    model = Post
    template_name = 'post/delete_post.html'
    success_url = reverse_lazy('blog_home')


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "post/index.html"
    paginate_by = 6


class PostDetail(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def post(self, request, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset)
        comments = post.comments.filter(approved=True).order_by("created_on")
        liked = False

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[pk]))

# class PostDetail(DetailView):
#
#     model = Post
#     template_name = 'post/post_detail.html'
#
#     def get(self, request, *args, **kwargs):
#         queryset = Post.objects.filter(status=1)
#         post = get_object_or_404(queryset)
#         comments = post.comments.filter(approved=True).order_by("-created_on")
#         liked = False
#         if post.likes.filter(id=self.request.user.id).exists():
#             liked = True
#
#         return render(
#             request,
#             "post/post_detail.html",
#             {
#                 "post": post,
#                 "comments": comments,
#                 "commented": False,
#                 "liked": liked,
#                 "comment_form": CommentForm()
#             },
#         )
#
#     def post(self, request, *args, **kwargs):
#
#         queryset = Post.objects.filter(status=1)
#         post = get_object_or_404(queryset)
#         comments = post.comments.filter(approved=True).order_by("created_on")
#         liked = False
#
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             comment_form.instance.email = request.user.email
#             comment_form.instance.name = request.user.username
#             comment = comment_form.save(commit=False)
#             comment.post = post
#             comment.save()
#         else:
#             comment_form = CommentForm()
#
#         return render(
#             request,
#             "post/post_detail.html",
#             {
#                 "post": post,
#                 "comments": comments,
#                 "commented": True,
#                 "comment_form": comment_form,
#                 "liked": liked
#             },
#         )
