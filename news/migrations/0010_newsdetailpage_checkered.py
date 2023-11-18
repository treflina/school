# Generated by Django 4.2.1 on 2023-11-18 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0009_alter_newsdetailpage_body_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsdetailpage",
            name="checkered",
            field=models.BooleanField(
                default=False,
                help_text="Wyśrodkowuje zdjęcie na stronie głównej i dodaje efekt kratki.\n        Przydatne do zdjęć o wysokości mniejszej niż tekst wprowadzający.",
                verbose_name="Tło zdjęcia w kratkę",
            ),
        ),
    ]
