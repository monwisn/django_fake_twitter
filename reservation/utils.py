from datetime import datetime as dtime, date, time
from calendar import HTMLCalendar
from pytz import timezone
from .models import Events, Event, CalendarEvent


class EventCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.events = events

    def formatday(self, day: int, weekday: int, events):
        """
        Return a day as a table cell.
        """
        events_from_day = events.filter(day__day=day)
        events_html = '<div style="height:120px;width:170px;overflow: auto">'
        for event in events_from_day:
            events_html += f'&nbsp;&nbsp; {event.get_html_url} &nbsp;&nbsp;({event.start_time:%H:%M} - {event.end_time:%H:%M}) &nbsp; <br/><br/>'
        if day == 0:
            return '<td class="date">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td></div>' % (self.cssclasses[weekday], day, events_html)

    def formatweek(self, theweek: int, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear: int, themonth: int, withyear: bool = True):
        """
        Return a formatted month as a table.
        """
        events = Event.objects.filter(day__month=themonth)

        v = []
        a = v.append
        a('<table border="3" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day: int, events):
        events_per_day = events.filter(start__day=day)
        d = '<div style="height:120px;width:150px;overflow: auto">'
        for event in events_per_day:
            d += f'{event.get_html_url}&nbsp;({event.start.time().strftime("%H:%M")} - {event.end.strftime("%H:%M %d/%m")})<br/><br/>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{d}</ul></td></div>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek: int, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr>{week}</tr><div/>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear: bool = True):
        events = Events.objects.filter(start__year=self.year, start__month=self.month)
        cal = f'<table border="2" cellpadding="10" cellspacing="30" class="month">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        cal += f'<table/>\n'

        return cal


class NewCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(NewCalendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = "<div style='height:120px;width:150px;overflow: auto;'>"
        for event in events_per_day:
            d += f"<li>Res.{event.id}:&nbsp;&nbsp; {event.get_html_url} </li>"
        if day != 0:
            return f"<td><span class='date'>&nbsp;&nbsp;&nbsp;{day}</span><ul> {d} </ul></td>"
        return "<td></td>"

    def formatweek(self, theweek, events):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f"<tr> {week} </tr><div/>"

    def formatmonth(self, withyear=True):
        events = CalendarEvent.objects.filter(
            start_time__year=self.year, start_time__month=self.month
        )
        cal = '<table border="0" cellpadding="0" cellspacing="0" class="calendar" style="font-size:13px">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        cal += f'<table/>\n'

        return cal
