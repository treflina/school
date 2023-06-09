from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

custom_table_options = {
    "renderer": "html",
    "contextMenu": {
        "items": {
            "row_above": {
                "name": "Wstaw wiersz powyżej",
            },
            "row_below": {
                "name": "Wstaw wiersz poniżej",
            },
            "col_left": {
                "name": "Wstaw kolumnę z lewej",
            },
            "col_right": {
                "name": "Wstaw kolumnę z prawej",
            },
            "remove_row": {
                "name": "Usuń wiersz",
            },
            "remove_col": {
                "name": "Usuń kolumnę",
            },
            "---------": {
                "name": "---------",
            },
            "undo": {
                "name": "Cofnij",
            },
            "redo": {
                "name": "Powtórz",
            },
        }
    },
}


class ContentBlock(blocks.StreamBlock):
    text = blocks.RichTextBlock(
        features=[
            "bold",
            "italic",
            "center",
            "right",
            "ol",
            "ul",
            "hr",
            "link",
            "document-link",
        ],
        label="Tekst",
        blank=True,
        # ////////////////////////////
        null=True,
    )
    image = ImageChooserBlock(blank=True, null=True, label="Zdjęcie")
    table = TableBlock(
        required=False,
        label="Tabela",
        template="home/table_block.html",
        table_options=custom_table_options,
    )


class RichtextAndTableBlock(blocks.StreamBlock):
    text = blocks.RichTextBlock(
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
        blank=True,
        # ////////////////////////////
        null=True,
    )
    table = TableBlock(
        required=False,
        label="Tabela",
        template="home/table_block.html",
        table_options=custom_table_options,
    )

    docs = blocks.ListBlock(
        DocumentChooserBlock(),
        required=False,
        label="Lista dokumentów do pobrania",
        template="streams/document_link_block.html",
    )


class ObjectAndDescriptionBlock(blocks.StructBlock):
    subject = blocks.CharBlock(label="Nazwa")
    description = blocks.ListBlock(
        blocks.CharBlock(), label="Imię i nazwisko"
    )

    class Meta:

        label = "Przedmiot (funkcja)"
        template = "streams/object_description_block.html"
