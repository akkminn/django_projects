from typing import Any
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required


from .models import User, AuctionList, Bid, Comment, Category


def index(request):
    active_list = AuctionList.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "active_list": active_list
    })

class DeatailsView(generic.DetailView):
    model = AuctionList
    template_name = "auctions/details.html"
    context_object_name = "list"
    
    def get_queryset(self):
        return super().get_queryset()
    
class WatchListView(generic.ListView):
    model = AuctionList
    template_name = "auctions/watchlists.html"
    context_object_name = "watchlist"

    def get_queryset(self):
        return self.request.user.watchlist.all()

@login_required
def add_to_watchlist(request, list_id):
    auction = get_object_or_404(AuctionList, id=list_id)
    request.user.watchlist.add(auction)
    return HttpResponseRedirect(reverse("listing", args=(list_id, )))

@login_required
def remove_from_watchlist(request, list_id):
    auction = get_object_or_404(AuctionList, id=list_id)
    request.user.watchlist.remove(auction)
    return HttpResponseRedirect(reverse("listing", args=(list_id, )))



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
