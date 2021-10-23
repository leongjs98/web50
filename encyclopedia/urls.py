from django.urls import path

from . import views


appname = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title")
]
