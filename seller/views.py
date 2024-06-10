from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Newsletter, BlogPost
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserRegistrationForm
from django.views.decorators.cache import cache_page


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


def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            return redirect('login')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


class ManagerDashboardView(View):
    def get(self, request):
        if not request.user.is_staff:
            return redirect('home')  # Redirect to home page for non-staff users

        return render(request, 'manager_dashboard.html')


@cache_page(60 * 15)  # Кеширование на 15 минут
def main_page(request):
    num_newsletters = Newsletter.objects.count()
    active_newsletters = Newsletter.objects.filter(status='active').count()
    num_unique_clients = Newsletter.objects.values('owner').distinct().count()
    random_blog_posts = BlogPost.objects.order_by('?')[:3]

    context = {
        'num_newsletters': num_newsletters,
        'active_newsletters': active_newsletters,
        'num_unique_clients': num_unique_clients,
        'random_blog_posts': random_blog_posts,
    }

    return render(request, 'main_page.html', context)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_post_detail.html'
    context_object_name = 'blog_post'

    def get_object(self):
        blog_post_id = self.kwargs.get('pk')
        return get_object_or_404(BlogPost, pk=blog_post_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_post = self.get_object()
        blog_post.views += 1  # Increment the number of views
        blog_post.save()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='manager').exists():
            return redirect('home')  # Redirect to home page for non-manager users
        return super().dispatch(request, *args, **kwargs)


def blog_post_list(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'blog_post_list.html', {'blog_posts': blog_posts})