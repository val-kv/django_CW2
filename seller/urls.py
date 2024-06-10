from django.urls import path
from .views import NewsletterListView, NewsletterCreateView, NewsletterDetailView, NewsletterUpdateView, \
    NewsletterDeleteView, main_page, BlogPostDetailView, blog_post_list
from . import views


app_name = 'seller'
urlpatterns = [
    path('newsletters/', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletters/<int:pk>/', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletters/<int:pk>/update/', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletters/<int:pk>/delete/', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('register/', views.register, name='register'),
    path('', main_page, name='main_page'),
    path('blog/', blog_post_list, name='blog_post_list'),
    path('blog/<int:pk>/', BlogPostDetailView.as_view(), name='blog_post_detail')
]
