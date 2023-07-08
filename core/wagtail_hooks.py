"""Richtext hooks."""
from django.utils.html import format_html
from django.templatetags.static import static

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
)

@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/mywagtail.css"))


@hooks.register("register_icons")
def register_icons(icons):
    """Creates additional icons to use in editor's interface and templates"""
    return icons + ["core/align-center.svg", "core/align-right.svg"]


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    """Creates centered text in the richtext editor and page."""

    feature_name = "center"
    type_ = "CENTERTEXT"
    tag = "div"

    control = {
        "type": type_,
        "icon": "text-centered",
        "description": "Wyśrodkuj",
        "style": {
            "display": "block",
            "text-align": "center",
        },
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_: {"element": tag, "props": {"class": "d-block text-center"}}
            }
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_alignright_feature(features):
    """Creates centered text in the richtext editor and page."""

    feature_name = "right"
    type_ = "ALIGNRIGHTTEXT"
    tag = "div"

    control = {
        "type": type_,
        "icon": "align-right",
        "description": "Do prawej",
        "style": {
            "display": "block",
            "text-align": "right",
        },
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_: {"element": tag, "props": {"class": "d-block text-right"}}
            }
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)
