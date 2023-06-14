from wagtail import blocks
from wagtail.templatetags.wagtailcore_tags import richtext
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock

custom_table_options = {
   'contextMenu': {
      'items': {
        "row_above": {
          'name': 'Wstaw wiersz powyżej',
        },
        "row_below": {
          'name': 'Wstaw wiersz poniżej',
        },
        "remove_row": {
          'name': 'supprimer une ligne',
        },
        "col_left": {
          'name': 'Wstaw kolumnę z lewej',
        },
        "col_right": {
          'name': 'Wstaw kolumnę z prawej',
        },
        "remove_row": {
          'name': 'Usuń wiersz',
        },
        "remove_col": {
          'name': 'Usuń kolumnę',
        },
        "---------": {
          'name': "---------",
        },
        "undo": {
          'name': 'Cofnij',
        },
        "redo": {
          'name': 'Powtórz',
        }
      }
    }
    }

class ContentBlock(blocks.StreamBlock):
    text = blocks.RichTextBlock(
        features=["bold", "italic", "ol", "ul", "link", "document-link", "hr"],
        label="Tekst",
    )
    image = ImageChooserBlock(label="Zdjęcie")
    table = TableBlock(
        required=False,
        label="Tabela",
        template="home/table_block.html",
        table_options=custom_table_options,
    )


class AccordionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, label="Nagłówek")
    content = ContentBlock(label="Treść")

    class Meta:  # noqa
        template = "home/accordion_block.html"
        icon = "placeholder"
        label = "Aktualność"
