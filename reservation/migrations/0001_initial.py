# Generated by Django 4.1.4 on 2023-03-29 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CalendarEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("booker_data", models.CharField(help_text="Name", max_length=200)),
                ("date", models.DateField(help_text="Event date")),
                ("start_time", models.TimeField(help_text="Starting time")),
                (
                    "duration",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (30, "30 minutes"),
                            (60, "1 hour"),
                            (90, "1.5 hours"),
                            (120, "2 hours"),
                        ],
                        default=60,
                    ),
                ),
                ("end_time", models.TimeField(help_text="Ending time")),
                (
                    "notes",
                    models.TextField(
                        blank=True, help_text="Add description", null=True
                    ),
                ),
                (
                    "cancellation_date",
                    models.BooleanField(default=False, help_text="Cancel your event?"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(help_text="Event title", max_length=150)),
                ("day", models.DateField(help_text="Event date")),
                ("start_time", models.TimeField(help_text="Starting time")),
                ("end_time", models.TimeField(help_text="Final time")),
                (
                    "location",
                    models.CharField(
                        blank=True,
                        help_text="Event location",
                        max_length=150,
                        null=True,
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True, help_text="Add description", null=True
                    ),
                ),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Scheduling",
            },
        ),
    ]