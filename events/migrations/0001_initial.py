# Generated by Django 4.2.1 on 2023-08-26 19:31

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0084_query_alter_page_title_searchpromotion_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventsPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
            ],
            options={
                "verbose_name": "Wydarzenia",
            },
            bases=("wagtailcore.page",),
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
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200, null=True, verbose_name="Nazwa wydarzenia"
                    ),
                ),
                ("start_date", models.DateField(verbose_name="Data")),
                (
                    "end_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Data zakończenia"
                    ),
                ),
                (
                    "hour",
                    models.TimeField(blank=True, null=True, verbose_name="Godzina"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="(Opcjonalnie) Krótki opis"
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="events.eventspage",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
    ]