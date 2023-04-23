from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Post, Category, Comment
from .forms import CommentForm, EditForm, PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages


class HomeBlogView(ListView):
    model = Post
    template_name = 'post/index.html'

    def get_queryset(self):
        cats = Category.objects.all()
        ordering = ['-created_on']
        queryset = Post.objects.order_by(*ordering)
        return queryset

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeBlogView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'post/category_list.html', {'cat_menu_list': cat_menu_list})


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    return render(request, 'post/categories.html', {
        'cats': cats.title().replace('-', ' '),
        'category_posts': category_posts
    })


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/add_post.html'

    def form_valid(self, form):
        messages.success(self.request, 'Post Created in the Blog!')
        return super().form_valid(form)


class AddCategoryView(CreateView):
    model = Category
    template_name = 'post/add_category.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'post/update_post.html'

    def form_valid(self, form):
        messages.success(self.request, 'Post updated!')
        return super().form_valid(form) 


class DeletePostView(DeleteView):
    model = Post
    template_name = 'post/delete_post.html'
    success_url = reverse_lazy('blog_home')

    def form_valid(self, form):
        messages.success(self.request, 'Your post was removed!')
        return super().form_valid(form)


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "post/index.html"
    paginate_by = 6


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        likes = self.object
        total_likes = likes.number_of_likes()
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        return context


class PostLike(View):

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/add_comment.html'
    success_url = reverse_lazy('blog_home')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        comment = form.save(commit=False)
        messages.success(self.request, 'Your comment is published!')

        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)

