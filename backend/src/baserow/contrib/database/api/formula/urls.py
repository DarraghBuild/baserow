from django.urls import re_path

from baserow.contrib.database.api.formula.views import TypeFormulaView

app_name = "baserow.contrib.database.api.export"

urlpatterns = [
    re_path(
        r"(?P<table_id>[a-z0-9_]+)/type/$",
        TypeFormulaView.as_view(),
        name="type_formula",
    ),
]
