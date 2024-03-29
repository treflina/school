# Generated by Django 4.2.1 on 2024-02-14 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0012_alter_newsdetailpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="minigalleryimage",
            name="alt_attr",
            field=models.CharField(
                blank=True,
                help_text="Opis tekstowy zdjęcia (najczęściej od 5 do 15 słów). Proszę nie pozostawiać bez opisu",
                max_length=255,
                verbose_name="Opis alternatywny",
            ),
        ),
        migrations.AlterField(
            model_name="newsdetailpage",
            name="alt_attr",
            field=models.CharField(
                blank=True,
                help_text="Proszę opisać co przedstawia zdjęcie. Pole nie powinno być puste\n        (wymóg dostępności cyfrowej stron internetowych instytucji publicznych). Jeżeli zdjęcie\n        zawiera informację tekstową, musi być ona zawarta również w tekstowej części artykułu lub ewentualnie w opisie\n        alternatywnym. To samo dotyczy pozostałych zdjęć w artykule. Więcej informacji:\n        https://www.uke.gov.pl/blog/tekst-alternatywny-do-grafik-i-zdjec-czyli-kilka-slow-o-altach,96.html",
                max_length=255,
                verbose_name="Opis alternatywny",
            ),
        ),
    ]
