from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, RedirectView, DetailView, ListView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

from blog.models import Post
from main.forms import AddForm, SignUpForm, TweetForm
from main.models import Profile, Book, Tweet, Chat
from main.common import UserAccessMixin

import openai


def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, 'Your Tweet Has Been Posted.')
                return redirect('main:home')

        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, 'main/home.html', {'tweets': tweets, 'form': form})
    else:
        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, 'main/home.html', {'tweets': tweets})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.all()
        # profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'main/profile_list.html', {'profiles': profiles})
    else:
        messages.info(request, 'You Must Be Logged In To View This Page...')
        return redirect('main:home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk)
        # PostForm logic
        if request.method == 'POST':
            # get current user ID
            current_user_profile = request.user.profile
            # get form data
            action = request.POST['follow']  # from profile.html button name='follow'
            # decide to follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)  # profile = pk
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            # save the profile
            current_user_profile.save()
        return render(request, 'main/profile.html', {'profile': profile, 'tweets': tweets})
    else:
        messages.info(request, 'You Must Be Logged In To View This Page...')
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
    # url = 'https://youtube.com/something/'
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
#     success_url = '/books/'  # this form view expecting us to have a user submit the form, and then
#     we're going to send them across to a new url
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


# class BookEditView(PermissionRequiredMixin, UpdateView):
#
#     raise_exception = False  # if True then 403 page will be shown and give use information that we need more permission
#     # to access to this link page and resources, for security reasons we should use False to provide a 404 page instead
#     # suggests that link doesn't exist
#     permission_required = ('main.change_book', 'main.add_book',)
#     # Permissions in Django follow the following naming sequence: {app}.{action}_{model_name}
#     # action can be: add, change, delete, view
#     permission_denied_message = ''
#     login_url = '/books/'  # we have control of where we want to send the user back after access is denied
#     redirect_field_name = 'next'  # we can just control this next item if we wanted to, redirect to next page
#
#     model = Book
#     form_class = AddForm
#     template_name = 'main/add-book.html'
#     success_url = '/books/'


class BookEditView(UserAccessMixin, UpdateView):
    raise_exception = False
    permission_required = 'main.change_book'
    permission_denied_message = ''
    login_url = '/books/'
    redirect_field_name = 'next'

    model = Book
    form_class = AddForm
    template_name = 'main/add-book.html'
    success_url = '/books/'


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    template_name = 'main/signup.html'
    success_url = reverse_lazy('main:home')
    success_message = 'Your profile was created successfully.'

    # def form_valid(self, form):
    #     user = form.save()
    #     if user is not None:
    #         login(self.request, user)
    #
    #     return super(SignUpView, self).form_valid(form)


# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password_1 = form.cleaned_data['password1']
#             password_2 = form.cleaned_data['password2']
#             email = form.cleaned_data['email']
#             birth_date = form.cleaned_data['birth_date']
#             user = authenticate(username=username, password=password_1)
#             login(request, user)
#             return redirect('main:home')
#     else:
#         form = SignUpForm()
#     return render(request, 'main/signup.html', {'form': form})


class LoginView(SuccessMessageMixin, FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('main:home')
    success_message = 'You\'re now logged in.'
    template_name = 'main/signin.html'
    redirect_field_name = REDIRECT_FIELD_NAME

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return self.render_to_response(self.get_context_data(form=form))


# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.info(request, f"You are now logged in as {username}.")
#             return redirect('main:home')
#         else:
#             return render(request, 'main/signin.html', {'error': 'Invalid Login credentials.'})
#     else:
#         return render(request, 'main/signin.html', {'error': 'Invalid login credentials.'})


class MyLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, 'You\' been successfully logged out.')
        return response


# def logout_view(request):
#     logout(request)
#     messages.info(request, f"You have been logged out!")
#     return redirect('main:home')


def ai_chat(request):
    user_input = ''
    ai_response = ''
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                user_input = request.POST.get('user_input')
                ai_response = generate_response(user_input)
                # saving user_input and ai_response in the database
                Chat.objects.create(user=request.user, user_input=user_input, ai_response=ai_response)

            # else:
            #     # if user didn't enter any input nothing should be sent
            #     user_input = ''
            #     ai_response = ''
            #     return redirect('main:chat')

            # displaying the chat history base on user
            chat_history = Chat.objects.filter(user=request.user)

            return render(request, 'main/chat.html',
                          {'user_input': user_input, 'chatbot_response': ai_response, 'chat_history': chat_history})

        else:
            messages.info(request, 'You Must Be Logged In To View This Page...')
            return redirect('main:home')

    except:
        return redirect('main:home')


openai.api_key = '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'


# Generating response from OpenAI Library
def generate_response(user_input):
    prompt = f'User: {user_input}'

    response = openai.Completion.create(
        model='text-davinci-002',
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response['choices'][0]['text']
    return message


# Clear chat
def clear_chat(request):
    # clear the chat conversation
    Chat.objects.all().delete()
    return redirect('main:chat')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = SignUpForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, 'Your Profile Has Been Updated.')
            return redirect('main:home')
        return render(request, 'main/update_user.html', {'form': form})

    else:
        messages.info(request, 'You Must Be Logged In To View That Page.')
        return redirect('main:home')
