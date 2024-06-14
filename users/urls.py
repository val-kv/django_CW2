from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.view_profile, name='profile'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
]