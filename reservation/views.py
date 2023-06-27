import calendar
import json
from datetime import datetime, date, timedelta

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import ListView, UpdateView

from .forms import CalendarEventForm, EventsForm, EventForm
from .models import Event, Events, CalendarEvent
from .utils import Calendar, EventCalendar


# def event(request):
#     form = EventForm(request.POST)
#     return render(request, 'reservation/event.html', {'form': form})


def add_event(request):
    form = CalendarEventForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.info(request, 'New Event Has Been Created.')
            return redirect('main:home')

    return render(request, 'reservation/event.html', {'form': form})


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


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('/'))
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


def event(request, event_id=None):
    instance = Events()
    if event_id:
        instance = get_object_or_404(Events, pk=event_id)
    else:
        instance = Events()
    form = EventsForm(request.POST or None, instance=instance)

    if request.POST and form.is_valid():
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


def some_func():
    raise NotImplementedError('something')


# def add_event(request):
    # form = CalendarEventForm(request.POST or None)
    # if request.method == "POST":
    #     if form.is_valid():
    #         form.save()
    #         messages.info(request, 'New Event Has Been Created.')
    #         return redirect('main:home')
    #
    # return render(request, 'reservation/event.html', {'form': form})

