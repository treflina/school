# Generated by Django 4.2.1 on 2023-07-03 15:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("wagtailcore", "0084_alter_page_title"),
    ]

    operations = [
        migrations.CreateModel(
            name="GalleryDetailPage",
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
                (
                    "main_text",
                    wagtail.fields.RichTextField(
                        blank=True,
                        help_text="Opcjonalny dodatkowy opis galerii.",
                        null=True,
                        verbose_name="Opis galerii",
                    ),
                ),
                (
                    "publish_date",
                    models.DateField(
                        blank=True,
                        default=django.utils.timezone.now,
                        help_text="Data publikacji wyświetlana na stronie.",
                        null=True,
                        verbose_name="Data publikacji",
                    ),
                ),
            ],
            options={
                "verbose_name": "Galeria zdjęć",
                "verbose_name_plural": "Galerie zdjęć",
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="GalleryIndexPage",
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
                "verbose_name": "Lista galerii zdjęć",
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="GalleryImage",
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
                    "alt_attr",
                    models.CharField(
                        blank=True,
                        help_text="Opis tekstowy zdjęcia (najczęściej od 5 do 15 słów) mający\n        na celu umożliwienie przekazu treści osobom słabowidzącym.",
                        max_length=255,
                        verbose_name="Opis alternatywny",
                    ),
                ),
                (
                    "highlight",
                    models.BooleanField(
                        default=False,
                        help_text="Wybrane zdjęcie będzie wyświetlone w wizytówce galerii",
                        verbose_name="Zdjęcie główne",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailimages.image",
                        verbose_name="",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery_images",
                        to="gallery.gallerydetailpage",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
    ]
