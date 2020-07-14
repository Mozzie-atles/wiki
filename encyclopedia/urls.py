from django.urls import path

from . import views
app_name = "wikip"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("/serch", views.search, name="search"),
    path("/new", views.newtab, name="newtab"),
    path("/", views.ranpage, name="random"),
    path("/Edit", views.edit, name="edit")
]
