from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from blog.models import BlogPost


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_post_detail.html'
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
            return redirect('main_page')  # Redirect to home page for non-manager users
        return super().dispatch(request, *args, **kwargs)


def blog_post_list(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'blog/blog_post_list.html', {'blog_posts': blog_posts})

