from django.shortcuts import render
from generic_chooser.views import ModelChooserViewSet
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.images.views.chooser import (
    ImageChooseResultsView,
    ImageChooserViewSet,
    ImageChooseView,
    BaseImageChooseView
)



class GalleryChooseView(ImageChooseView, BaseImageChooseView):
    per_page = 30


class GalleryChooseResultsView(ImageChooseResultsView):
    per_page = 30


class GalleryChooserViewSet(ImageChooserViewSet):
    model = "wagtailimages.Image"
    per_page = 30
    choose_view_class = GalleryChooseView
    choose_results_view_class = GalleryChooseResultsView


gallery_chooser_viewset = GalleryChooserViewSet("gallery_images")
