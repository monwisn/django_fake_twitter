from datetime import datetime, timedelta, time

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Events(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        url = reverse('reservation:edit_event', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ('start',)

    def clean(self):
        start_date = self.start
        end_date = self.end

        if end_date <= start_date:
            raise ValidationError({"end": "End date must be later than start date"})
        elif start_date <= datetime.now():
            raise ValidationError({"start": "You can't choose a date in the past."})

        return super(Events, self).clean()


class Event(models.Model):
    title = models.CharField(max_length=150)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=150, blank=True, null=True)
    notes = models.TextField(help_text='Add description', blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        url = reverse('reservation:edit_show_events', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Scheduling'
        ordering = ('-day', 'start_time')

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):  # overlapping events
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (fixed_start <= new_start <= fixed_end) or (fixed_start <= new_end <= fixed_end):  # inner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outer limits
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])

        return '<a href="%s">No. %s: %s (%s - %s)</a><br/>' % (
            url, str(self.id), str(self.title), str(self.start_time.strftime("%H:%M")),
            str(self.end_time.strftime("%H:%M")))

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("Ending time must be after starting time.", code="invalid")

        if (self.day.strftime("%Y/%m/%d ") + self.start_time.strftime("%H:%M:%S")) <= datetime.now().strftime(
                "%Y/%m/%d %H:%M:%S"):
            raise ValidationError("You can't choose a date in the past.", code="invalid")

        events = Event.objects.filter(day=self.day).exclude(id=self.id)
        # events = Event.objects.filter(day=self.day)

        if events.exists():
            for event in events:
                # if event.id != self.id:
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError(f"""There is an overlap event with this date:\
                                          {event.day.strftime("%d/%m/%Y")},\
                                          {event.start_time.strftime("%H:%M")} - {event.end_time.strftime("%H:%M")}.""",
                                          code='invalid')
        super(Event, self).clean()

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)


class CalendarEventDuration(models.IntegerChoices):
    HALF_HOUR = 30, "30 minutes"
    ONE_HOUR = 60, "1 hour"
    ONE_AND_A_HALF_HOURS = 90, "1.5 hours"
    TWO_HOURS = 120, "2 hours"


class CustomDateTimeField(models.DateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            val.replace(microsecond=0)
            return val.isoformat()
        return ''


class CalendarEvent(models.Model):
    booker_data = models.CharField(max_length=200, help_text='Name and Surname')
    start_time = models.DateTimeField(help_text='Starting time',
                                      default=datetime.now)  # or datetime.now to get current time when refresh
    duration = models.PositiveSmallIntegerField(default=CalendarEventDuration.ONE_HOUR,
                                                choices=CalendarEventDuration.choices)  # DurationField()
    end_time = CustomDateTimeField(help_text='Final time', default=datetime.now, editable=True)
    notes = models.TextField(help_text='Add description', blank=True, null=True)
    cancel_event = models.BooleanField(help_text='Cancel this event', default=False)

    # def validate_dates(self, data):
    #     if data['start_time'] >= data['end_time']:
    #         raise ValidationError("Finish must occur after start.")
    #     return data

    def clean(self):
        # extra validation to ensure that the start date is always in the future.
        if self.start_time <= datetime.now():
            raise ValidationError("Start time cannot be in the past.")

    def save(self, *args, **kwargs):
        """ On save, update end_time """
        self.end_time = self.start_time + timedelta(minutes=self.duration)
        return super(CalendarEvent, self).save(*args, **kwargs)

    def __str__(self):
        return f'Reservation {self.id}: {self.booker_data}'
