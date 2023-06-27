from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('', views.add_event, name='add_event'),
    # path('event/', views.event, name='event'),
    path('events/', views.EventsView.as_view(), name='events'),
    path('events/new/', views.event, name='new_event'),
    path('events/edit/<int:event_id>', views.event, name='edit_event'),
    path('show_events/', views.ShowEventsView.as_view(), name='show_events'),
    path('show_events/new/', views.show_events, name='new_show_events'),
    path('show_events/edit/<int:event_id>', views.show_events, name='edit_show_events'),
]
