from wagtail import hooks

from .views import gallery_chooser_viewset


@hooks.register("register_admin_viewset")
def register_viewset():
    return gallery_chooser_viewset
