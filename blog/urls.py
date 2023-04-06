from . import views
from django.urls import path


urlpatterns = [
    path('blog/', views.PostList.as_view(), name='blog_home'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('like/<int:pk>', views.PostLike.as_view(), name='post_like'),
    path('detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('detail/edit/<int:pk>', views.UpdatePostView.as_view(), name='update_post'),
    path('detail/<int:pk>/remove', views.DeletePostView.as_view(), name='delete_post'),
    path('category/<str:cats>/', views.CategoryView, name='category'),
    path('category-list/', views.CategoryListView, name='category_list'),
    path('detail/<int:pk>/comment/', views.AddCommentView.as_view(), name='add_comment')

]
