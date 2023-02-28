from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from simple_chatbot.views import SimpleChatbot

import blog.views
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('add-post/', blog.views.AddPostView.as_view(), name='add_post'),
    path('profile-list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>/', views.profile, name='profile'),

    # extra context Attribute from ContentMixin = keyword argument for as_view()
    # path('ex1/', views.TemplateView.as_view(template_name='ex1.html', extra_context={'title': 'Custom Title'})),
    path('ex2/', views.Ex2View.as_view(), name='ex2'),
    path('redirect/', RedirectView.as_view(url='https://youtube.com/veryacademy'), name='go_to_url'),
    path('ex3/<int:pk>/', views.PostPreLoadTaskView.as_view(), name='redirect_task'),
    path('ex4/<int:pk>/', views.SinglePostView.as_view(), name='single_post'),   # single post page
    path('books/', views.BookView.as_view(), name='books'),
    path('books/add/', views.AddBookView.as_view(), name='add_book'),
    path('books/<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/genre/<str:genre>/', views.GenreView.as_view(), name='genre'),
    path('books/<slug:slug>/edit/', views.BookEditView.as_view(), name='book_edit'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    # path('logout/', LogoutView.as_view(next_page="main:home"), name='logout'),
    path('chatbot/', views.ai_chat, name='chat'),
    path('clear-chat/', views.clear_chat, name='clear'),
    path('update-user/', views.update_user, name='update_user'),
    # path('simple_chatbot/', SimpleChatbot.as_view(), name='chatbot'),
]
