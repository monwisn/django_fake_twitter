from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms

from reservation.models import CalendarEvent, Event, Events


class CustomDateTimePickerInput(DateTimePickerInput):
    _date_format = "%Y-%m-%d %H:%M"
    backend_date_format = "YYYY-MM-DD HH:mm"


class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ('booker_data', 'start_time', 'duration', 'notes', 'cancel_event')
        help_texts = {
            'booker_data': '',
            'start_time': '',
            'notes': '',
            'cancel_event': '(Do you want to cancel your event?)',
        }

        widgets = {
            'booker_data': forms.TextInput(attrs={'class': 'form-control',
                                                  'placeholder': 'Enter your first and last name'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input',
                                                     'data-target': '#datetimepicker1',
                                                     'placeholder': 'dd-mm-yyyy,  --:--'}),
            # 'start_time': CustomDateTimePickerInput(),
            'duration': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add your event description'}),
            'cancel_event': forms.CheckboxInput(),
            # "end_time": DateTimePickerInput(range_from="start_time"),
        }


class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventsForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end'].input_formats = ('%Y-%m-%dT%H:%M',)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
            'day': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'end_time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%H:%M',)
        self.fields['end_time'].input_formats = ('%H:%M',)
