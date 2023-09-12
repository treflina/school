# Generated by Django 4.2.1 on 2023-09-12 18:31

from django.db import migrations
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.contrib.typed_table_block.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_alter_accessibilityinfopage_architecture_desc_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ordinarypage",
            name="content",
            field=wagtail.fields.StreamField(
                [
                    (
                        "text",
                        wagtail.blocks.RichTextBlock(
                            blank=True,
                            features=[
                                "h2",
                                "h3",
                                "bold",
                                "italic",
                                "center",
                                "right",
                                "ol",
                                "ul",
                                "hr",
                                "link",
                                "document-link",
                                "image",
                            ],
                            label="Tekst",
                            null=True,
                        ),
                    ),
                    (
                        "table",
                        wagtail.contrib.table_block.blocks.TableBlock(
                            label="Tabela",
                            required=False,
                            table_options={
                                "contextMenu": {
                                    "items": {
                                        "---------": {"name": "---------"},
                                        "col_left": {"name": "Wstaw kolumnę z lewej"},
                                        "col_right": {"name": "Wstaw kolumnę z prawej"},
                                        "redo": {"name": "Powtórz"},
                                        "remove_col": {"name": "Usuń kolumnę"},
                                        "remove_row": {"name": "Usuń wiersz"},
                                        "row_above": {"name": "Wstaw wiersz powyżej"},
                                        "row_below": {"name": "Wstaw wiersz poniżej"},
                                        "undo": {"name": "Cofnij"},
                                    }
                                },
                                "renderer": "html",
                            },
                            template="streams/table_block.html",
                        ),
                    ),
                    (
                        "typed_table",
                        wagtail.contrib.typed_table_block.blocks.TypedTableBlock(
                            [
                                (
                                    "text",
                                    wagtail.blocks.CharBlock(label="Krótki tekst."),
                                ),
                                (
                                    "long_text",
                                    wagtail.blocks.TextBlock(label="Długi tekst."),
                                ),
                                (
                                    "rich_text",
                                    wagtail.blocks.RichTextBlock(
                                        features=[
                                            "bold",
                                            "italic",
                                            "ol",
                                            "ul",
                                            "text-green",
                                            "text-violet",
                                            "text-red",
                                            "text-orange",
                                            "image",
                                            "link",
                                        ],
                                        label="Tekst z edycją",
                                    ),
                                ),
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        label="Obraz"
                                    ),
                                ),
                            ],
                            label="Tabela z dodatkową edycją komórek",
                            required=False,
                            table_options={
                                "contextMenu": {
                                    "items": {
                                        "---------": {"name": "---------"},
                                        "col_left": {"name": "Wstaw kolumnę z lewej"},
                                        "col_right": {"name": "Wstaw kolumnę z prawej"},
                                        "redo": {"name": "Powtórz"},
                                        "remove_col": {"name": "Usuń kolumnę"},
                                        "remove_row": {"name": "Usuń wiersz"},
                                        "row_above": {"name": "Wstaw wiersz powyżej"},
                                        "row_below": {"name": "Wstaw wiersz poniżej"},
                                        "undo": {"name": "Cofnij"},
                                    }
                                },
                                "renderer": "html",
                            },
                            template="streams/typed_table_block.html",
                        ),
                    ),
                    (
                        "docs",
                        wagtail.blocks.ListBlock(
                            wagtail.documents.blocks.DocumentChooserBlock(),
                            label="Dokumenty do pobrania",
                            required=False,
                            template="streams/document_link_block.html",
                        ),
                    ),
                ],
                blank=True,
                null=True,
                use_json_field=True,
                verbose_name="Treść",
            ),
        ),
    ]
