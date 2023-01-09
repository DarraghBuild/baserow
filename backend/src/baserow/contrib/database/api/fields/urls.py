from django.urls import re_path

from baserow.contrib.database.fields.registries import field_type_registry

from .views import (
    AsyncDuplicateFieldView,
    FieldsView,
    FieldView,
    UniqueRowValueFieldView,
)

app_name = "baserow.contrib.database.api.fields"

urlpatterns = field_type_registry.api_urls + [
    re_path(r"table/(?P<table_id>[a-z0-9_]+)/$", FieldsView.as_view(), name="list"),
    re_path(
        r"(?P<field_id>[a-z0-9_]+)/unique_row_values/$",
        UniqueRowValueFieldView.as_view(),
        name="unique_row_values",
    ),
    re_path(r"(?P<field_id>[a-z0-9_]+)/$", FieldView.as_view(), name="item"),
    re_path(
        r"(?P<field_id>[a-z0-9_]+)/duplicate/async/$",
        AsyncDuplicateFieldView.as_view(),
        name="async_duplicate",
    ),
]
