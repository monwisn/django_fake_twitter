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
