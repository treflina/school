from wagtail.documents.models import Document, AbstractDocument
from wagtail.models import Page

from .utils import convert_bytes, extract_extension



class CustomDocument(AbstractDocument):
    @property
    def get_extension(self):
        return extract_extension(self.file)

    @property
    def get_size(self):
        return convert_bytes(self.file_size)

    admin_form_fields = Document.admin_form_fields


class IndexPage(Page):

    template = "core/index_page.html"
    desription = "Strona nadrzędna (np. 'O szkole', 'Galerie') - listująca podstrony"

    @property
    def get_child_pages(self):
        return self.get_children().public().live()

    class Meta:
        verbose_name = "Strona nadrzędna"