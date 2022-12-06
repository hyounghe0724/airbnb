from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.CategoryViewSet.as_view(
            {"get": "list", "post": "create"},
        ),
    ),  # if import class other file(in case view.py) class of file, write as_view
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {"get": "retrieve", "put": "partial_update", "delete": "destroy"},
        ),
    ),
]
