from django.urls import path

from . import views


app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),    # Must be this before searching for title
    path("wiki/<str:title>", views.title, name="title")
]
