from django.urls import path

from blog.views import blog_post_list, BlogPostDetailView

urlpatterns = [
    path('blog/', blog_post_list, name='blog_post_list'),
    path('blog/<int:pk>/', BlogPostDetailView.as_view(), name='blog_post_detail'),
]
