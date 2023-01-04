from django.urls import path

import blog.views
from . import views


app_name = 'main'

urlpatterns = [
    path("", views.home, name='home'),
    path('add-post/', blog.views.AddPostView.as_view(), name='add_post'),
]
