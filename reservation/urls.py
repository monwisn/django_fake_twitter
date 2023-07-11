from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    # path("calendar-show/", views.CalendarViewShow.as_view(), name="calendar_show"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
    path('event/add/', views.add_event, name='add_event'),
    path('event/edit/<int:pk>/', views.EventEdit.as_view(), name="event_edit"),
    path('event/<int:event_id>/details/', views.event_details, name='event_details'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('all-event-list/', login_required(views.EventListView.as_view(), login_url='main:login'), name='all_event'),
    path('running-event-list/', views.RunningEventListView.as_view(), name='running_event'),
    path('calendar-dashboard/', views.DashboardView.as_view(), name='calendar_dashboard'),
    path('search-event/', views.search_event, name='search_event'),

    path('events/', views.EventsView.as_view(), name='events'),
    path('events/new/', views.event, name='new_events'),
    path('events/edit/<int:event_id>', views.event, name='edit_events'),

    path('show-events/', views.ShowEventsView.as_view(), name='show_events'),
    path('show-events/new/', views.show_events, name='new_show_events'),
    path('show-events/edit/<int:event_id>', views.show_events, name='edit_show_events'),
]
