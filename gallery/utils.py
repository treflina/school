def get_banner_image(q):
    """Returns an image to display as thumbnail eg. on listing pages"""
    for gallery in q:
        gallery.page_type = "gallery"
        banner_images = gallery.gallery_images.all()

        banner_image = banner_images.filter(highlight=True).last()
        if banner_image:
            gallery.banner_image = banner_image.image
        else:
            if len(banner_images) > 1:
                gallery.banner_image = banner_images.last().image
    return q
