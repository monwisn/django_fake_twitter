import calendar
import json
from datetime import datetime, date, timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import ListView, UpdateView, View

from .forms import CalendarEventForm, EventsForm, EventForm
from .models import Event, Events, CalendarEvent
from .utils import Calendar, EventCalendar, NewCalendar


class ShowEventsView(ListView):
    model = Event
    template_name = 'reservation/show-events.html'

    def get_context_data(self, context=None, **kwargs):
        after_day = self.request.GET.get('day__gte', None)
        context = context or {}

        if not after_day:
            d = date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = date.today()

        previous_month = date(year=d.year, month=d.month, day=1)
        previous_month = previous_month - timedelta(days=1)
        previous_month = date(year=previous_month.year, month=previous_month.month, day=1)

        last_day = calendar.monthrange(d.year, d.month)
        next_month = date(year=d.year, month=d.month, day=last_day[1])
        next_month = next_month + timedelta(days=1)
        next_month = date(year=next_month.year, month=next_month.month, day=1)

        context['previous_month'] = 'day__gte=' + str(previous_month)
        context['next_month'] = 'day__gte=' + str(next_month)

        cal = EventCalendar()
        html_cal = cal.formatmonth(d.year, d.month, withyear=True)
        html_cal = html_cal.replace('<td ', '<td  width="150" height="150"')
        context['calendar'] = mark_safe(html_cal)

        return context


class EventsView(ListView):
    model = Events
    template_name = 'reservation/events-calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('/'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '/' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = f'month={next_month.year}/{next_month.month}'
    return month


class CalendarView(ListView):
    model = CalendarEvent
    template_name = "reservation/event-reservation-calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = NewCalendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


class EventListView(ListView):
    """ All event list views """

    template_name = "reservation/event-list.html"
    model = CalendarEvent

    def get_queryset(self):
        return CalendarEvent.objects.get_all_events().order_by('-start_time')
        # return CalendarEvent.objects.get_all_events(user=self.request.user)  # if user exists/login required


class RunningEventListView(ListView):
    """ Running event list view """

    template_name = "reservation/event-list.html"
    model = CalendarEvent

    def get_queryset(self):
        return CalendarEvent.objects.get_running_events().order_by('-start_time')
        # return CalendarEvent.objects.get_running_events(user=self.request.user)  # same as above


class DashboardView(View):
    template_name = "reservation/reservation-dashboard.html"

    def get(self, request, *args, **kwargs):
        events = CalendarEvent.objects.get_all_events()
        running_events = CalendarEvent.objects.get_running_events()
        latest_events = CalendarEvent.objects.order_by("-id")[:10]
        context = {
            "total_events": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
            "past_events": events.count() - running_events.count()
        }
        return render(request, self.template_name, context)

# def create_event(request):
#     form = CalendarEventForm(request.POST or None)
#     if request.POST:
#         if form.is_valid():
#             booker_data = form.cleaned_data["booker_data"]
#             start_time = form.cleaned_data["start_time"]
#             duration = form.cleaned_data["duration"]
#             end_time = form.cleaned_data["end_time"]
#             notes = form.cleaned_data["notes"]
#
#             CalendarEvent.objects.get_or_create(
#                 booker_data=booker_data,
#                 duration=duration,
#                 start_time=start_time,
#                 end_time=end_time,
#                 notes=notes,
#             )
#         return HttpResponseRedirect(reverse("reservation:calendar_show"))
#     return render(request, "reservation/event.html", {"form": form})


def add_event(request):
    form = CalendarEventForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.info(request, 'New Event has been created.')
        # return redirect('main:home')
        return redirect('reservation:calendar')
    return render(request, 'reservation/event.html', {'form': form})


def delete_event(request, event_id):
    event = get_object_or_404(CalendarEvent, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.info(request, f'Reservation "{event.booker_data[:30]}..." has been deleted.')
        return redirect('reservation:calendar')
    return render(request, 'reservation/event-delete.html', {'event': event})


class EventEdit(UpdateView):
    model = CalendarEvent
    form_class = CalendarEventForm
    # fields = ["booker_data", "duration", "start_time", "notes"]
    template_name = 'reservation/event.html'

    # def form_valid(self, form):
    #     if form.cleaned_data['start_time'] <= datetime.now():
    #         form.add_error("start_time", "You can't edit past events.")
    #         return self.form_invalid(form)
    #     return super(EventEdit, self).form_valid(form)


def event_details(request, event_id):
    event = CalendarEvent.objects.get(id=event_id)
    return render(request, "reservation/event-details.html", {'event': event})


# class CalendarViewShow(View):
#     template_name = "reservation/event-reservation-calendar.html"
#     form_class = CalendarEventForm
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         events = CalendarEvent.objects.get_all_events()
#         events_month = CalendarEvent.objects.get_running_events()
#         event_list = []
#
#         for event in events:
#             event_list.append(
#                 {
#                     "booker_data": event.booker_data,
#                     "start": event.start_time.strftime("%Y-%m-%dT%H:%M"),
#                     "end": event.end_time.strftime("%Y-%m-%dT%H:%M"),
#                     "notes": event.notes,
#                 }
#             )
#         context = {"form": form, "event_list": event_list, "events_month": events_month}
#         return render(request, self.template_name, context)
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("reservation:calendar_show")
#
#         return render(request, self.template_name, {'form': form})


def event(request, event_id=None):
    instance = Events()
    if event_id:
        instance = get_object_or_404(Events, pk=event_id)
    else:
        instance = Events()
    form = EventsForm(request.POST or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.info(request, f'"{instance.title}" event has been added.')
        return HttpResponseRedirect(reverse('reservation:events'))
    return render(request, 'reservation/calendar-event.html', {'form': form})


def show_events(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    form = EventForm(request.POST or None, instance=instance)

    if request.POST:
        if form.is_valid():
            form.save()
            messages.info(request, f'Your Event "{instance.title[:20]}..." Has Been Added.')
            return HttpResponseRedirect(reverse('reservation:show_events'))
        else:
            messages.error(request, 'Please correct the error below.')
            # for error in list(form.errors.values()):
            #     messages.error(request, error)
    return render(request, 'reservation/calendar.html', {'form': form})


def search_event(request):
    if request.method == 'POST':
        search_reservation = request.POST['search']
        searched = CalendarEvent.objects.filter(booker_data__contains=search_reservation)
        return render(request, 'reservation/search-event.html', {'search_reservation': search_reservation, 'searched': searched})
    else:
        reservation = CalendarEvent.objects.all().order_by("-start_time")
        return render(request, 'reservation/search-event.html', {'reservation': reservation})


def some_func():
    raise NotImplementedError('something')
