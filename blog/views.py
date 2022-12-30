from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from blog.models import Post


class HomeView(ListView):
    model = Post
    # template_name = 'blog/index.html'
    context_object_name = "posts"
    # context_object_name: this is reference to the data that is being collected from this class here or this view
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            return "components/post-list-elements.html"
        return 'blog/index.html'


def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    related = Post.objects.filter(author=post.author)[:5]
    return render(request, 'blog/single_post.html', {'post': post, 'related': related})


class TagListView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'

    def get_queryset(self):
        # x = Post.objects.filter(tags__name=self.kwargs['tag'])
        x = Post.objects.filter(tags__name__in=[self.kwargs['tag']])
        print(x)

        return x

    def get_template_names(self):
        if self.request.htmx:
            return "components/post-list-elements-tags.html"

        return 'blog/tags.html'

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']

        return context