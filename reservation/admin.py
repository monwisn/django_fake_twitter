import calendar
import datetime

# from calendar import HTMLCalendar
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .utils import EventCalendar
from .models import Event, CalendarEvent, Events


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    fields = ['title', 'day', 'start_time', 'end_time', 'location', 'notes']
    list_display = ['title', 'day', 'start_time', 'end_time', 'location', 'notes']
    list_filter = ['day', 'location']
    search_fields = ['id', 'day', 'location', 'title']
    change_list_template = 'admin/change_list.html'

    def changelist_view(self, request, extra_context=None):
        after_day = request.GET.get('day__gte', None)
        extra_context = extra_context or {}

        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = datetime.date.today()

        previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
        previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                       day=1)  # find first day of previous month

        last_day = calendar.monthrange(d.year, d.month)
        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
        next_month = next_month + datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month,
                                   day=1)  # find first day of next month

        extra_context['previous_month'] = reverse('admin:reservation_event_changelist') + '?day__gte=' + str(
            previous_month)
        extra_context['next_month'] = reverse('admin:reservation_event_changelist') + '?day__gte=' + str(next_month)

        # cal = HTMLCalendar()
        cal = EventCalendar()
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['calendar'] = mark_safe(html_calendar)
        return super(EventAdmin, self).changelist_view(request, extra_context)


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    model = CalendarEvent
    fields = ['booker_data', 'start_time', 'duration', 'end_time', 'notes', 'cancel_event']
    list_display = [f.name for f in CalendarEvent._meta.get_fields()]
    list_filter = ['duration', 'cancel_event']
    search_fields = ['id', 'booker_data']
    readonly_fields = ['end_time']


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    model = Events
    list_display = ['title', 'description', 'start', 'end']
    # list_display = [f.name for f in Calendar._meta.fields]
