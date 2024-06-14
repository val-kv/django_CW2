from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from blog.models import BlogPost
from .models import Newsletter
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.cache import cache


class NewsletterListView(ListView):
    model = Newsletter
    template_name = 'newsletter_list.html'
    context_object_name = 'newsletters'

    def get_queryset(self):
        user = self.request.user
        return Newsletter.objects.filter(owner=user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='manager').exists():
            return redirect('home')  # Redirect to home page for non-manager users
        return super().dispatch(request, *args, **kwargs)

    @login_required
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:  # Проверка для суперпользователя
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('home')  # Редирект для пользователей с другими ролями


class NewsletterCreateView(CreateView):
    model = Newsletter
    template_name = 'newsletter_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('newsletter_list')


class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = 'newsletter_detail.html'


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    template_name = 'newsletter_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('newsletter_list')


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    template_name = 'newsletter_confirm_delete.html'
    success_url = reverse_lazy('newsletter_list')


class ManagerDashboardView(View):
    def get(self, request):
        if not request.user.is_staff:
            return redirect('home')  # Redirect to home page for non-staff users

        return render(request, 'manager_dashboard.html')


def main_page(request):
    cached_content = cache.get('main_page_content')
    if not cached_content:
        blog_posts = BlogPost.objects.all()
        cached_content = blog_posts
        cache.set('blog_posts_content', cached_content, 60 * 60)  # Cache for 1 hour
        newsletters = Newsletter.objects.all()
        cached_content = newsletters
        cache.set('newsletters_content', cached_content, 60 * 60)  # Cache for 1 hour
    return render(request, 'main_page.html', {'blog_posts': cached_content},
                  {'newsletters': cached_content})
