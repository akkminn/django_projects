from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("newEntry/", views.newEntry, name="newEntry"),
    path("edit/", views.edit, name="edit"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("random/", views.randomEntry, name="random"),
    path("delete/<str:title>", views.deletePage, name="delete")
]
