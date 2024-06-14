from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:pk>", views.DeatailsView.as_view(), name="listing"),
    path("watchlists/", views.WatchListView.as_view(), name="watchlists"),
    path("watchlists/add/<int:list_id>/", views.add_to_watchlist, name="add"),
    path("wathclists/remove/<int:list_id>/", views.remove_from_watchlist, name="remove")
]
