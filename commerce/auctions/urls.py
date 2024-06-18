from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:list_id>", views.details, name="listing"),
    path("watchlists/", views.WatchListView.as_view(), name="watchlists"),
    path("watchlists/add/<int:list_id>/", views.add_to_watchlist, name="add"),
    path("wathclists/remove/<int:list_id>/", views.remove_from_watchlist, name="remove"),
    path("create/", views.create, name="create"),
    path("close/<int:list_id>", views.close, name="close"),
    path("placebid/<int:list_id>", views.place, name="placebid"),
    path("bycategory/", views.displayByCategory, name="bycategory"),
    path("comment/<int:list_id>", views.comment, name="comment")
]
