from django.contrib import messages
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView, RedirectView, DetailView, ListView
from django.views.generic.edit import FormView, CreateView, UpdateView

from blog.models import Post
from main.forms import AddForm
from main.models import Profile, Book


def home(request):
    return render(request, 'main/home.html')
    # return HttpResponse('Hello world')


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'main/profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, 'You Must Be Logged In To View This Page...')
        return redirect('main:home')


class Ex2View(TemplateView):

    """ TemplateResponseMixin
    Provides a mechanism to construct a TemplateResponse, given suitable context.
    Attributes:
    """
    template_name = 'ex2.html'
    # template_engine = The NAME of a template engine to use for loading the template.
    # response_class = Custom template loading or custom context object instantiation
    # content_type = Default Django uses 'text/html'

    """ get_context_data(**kwargs) is a method inherited from ContentMixin """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        # context['posts'] = Post.objects.get(id=1)
        context['data'] = 'Context Data for Ex2'
        return context


class PostPreLoadTaskView(RedirectView):
    # url = 'https://youtube.com/veryacademy/'
    pattern_name = 'main:single_post'
    # permanent = HTTP status code returned (True = 301, False = 302, Default = False)

    def get_redirect_url(self, *args, **kwargs):  # reverse the pattern_name if URL is not set
        post = Post.objects.filter(pk=kwargs['pk'])
        post.update(count=F('count') + 1)

        return super().get_redirect_url(*args, **kwargs)


class SinglePostView(TemplateView):
    template_name = 'ex4.html'  # single post view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = get_object_or_404(Post, pk=self.kwargs.get('pk'))  # pk to identify single post

        return context


# class AddBookView(FormView):   # FormView
#     template_name = 'main/add-book.html'
#     form_class = AddForm  # that's going to be the form that we're going to build
#     success_url = '/books/'  # this form view expecting us to have a user submit the form and then we're going to send them across to a new url
#
#     def from_valid(self, form):
#         form.save()
#         return super().form_valid(form)

class AddBookView(CreateView):
    model = Book
    form_class = AddForm
    # fields = ['title', 'genre', 'author', 'isbn',]
    template_name = 'main/add-book.html'
    success_url = '/books/'

    # def get_initial(self, *args, **kwargs):
    #     initial = super().get_initial(**kwargs)
    #     initial['title'] = 'Enter Title'
    #     return initial


# class BookView(TemplateView):
#     template_name = 'main/books.html'
#
#     # get_context_data- context is additional information that we want to pass back to the template
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['books'] = Book.objects.all()
#         return context


class BookView(ListView):
    model = Book
    template_name = 'main/books.html'
    context_object_name = 'books'  # using ListView default name of context is object_list instead of object in template
    paginate_by = 8
    ordering = ['-id']
    # queryset = Book.objects.all()[:8]  # we can limit the amount of items that are displayed

    # def get_queryset(self):
    #     return Book.objects.all().order_by('id')  # the same queryset operation as above


class BookDetailView(DetailView):
    model = Book
    template_name = 'main/book-detail-view.html'
    context_object_name = 'book'  # default name is 'object' and we can use this in template e.g. {{ object.title }}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = Book.objects.filter(slug=self.kwargs.get('slug'))
        post.update(count=F('count') + 1)

        context['time'] = timezone.now()

        return context


class GenreView(ListView):
    model = Book
    template_name = 'main/books.html'
    context_object_name = 'books'
    paginate_by = 2  # Pagination over-write

    def get_queryset(self, *args, **kwargs):
        return Book.objects.filter(genre__icontains=self.kwargs.get('genre'))


class BookEditView(UpdateView):
    model = Book
    form_class = AddForm
    template_name = 'main/add-book.html'
    success_url = '/books/'
