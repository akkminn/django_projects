from queue import Full
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
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "active_list": active_list,
        "categories": categories
    })

class DeatailsView(generic.DetailView):
    model = AuctionList
    template_name = "auctions/details.html"
    context_object_name = "list"
    
    def get_queryset(self):
        return AuctionList.objects.filter(is_active=True)

    
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

def displayByCategory(request):
    if request.method == "POST":
        category = request.POST["category"]        
        categories = Category.objects.all()
        if category == "None":
            active_listings = AuctionList.get_none_category().filter(is_active=True)
            return render(request, "auctions/index.html", {
            "active_list": active_listings,
            "categories": categories
        })
        else:
            categorylist = Category.objects.get(name=category)
            active_listings = AuctionList.objects.filter(is_active=True, category=categorylist)
            return render(request, "auctions/index.html", {
                "active_list": active_listings,
                "categories": categories
            })


@login_required
def create(request):
    if request.method == "POST":

        # Get the data
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        image_url = request.POST["imageURL"]
        category = request.POST["category"]

        bid = Bid(
            bid=int(bid),
            user=request.user
        )
        bid.save()

        if category == "None":
            new_list = AuctionList(
                title = title,
                description = description,
                current_bid = bid,
                imageURL = image_url,
                owner = request.user,
                category = None
            )
            new_list.save()
        
        else:
            categorydata = Category.objects.get(name=category)
            new_list = AuctionList(
                title = title,
                description = description,
                current_bid = bid,
                imageURL = image_url,
                owner = request.user,
                category = categorydata
            )
            new_list.save()

        categories = Category.objects.all()
        return HttpResponseRedirect(reverse("index"), categories) 
    
    categories = Category.objects.all()
    return render(request, "auctions/create.html", {
        "categories": categories
    })

@login_required
def close(request, list_id):
    list = get_object_or_404(AuctionList, id=list_id)
    list.is_active = False
    list.save()
    if request.user == list.current_bid.user:
        return render(request, "auctions/details.html", {
            "message": "Congrats! You won the auctions.",
            "success": True,
            "list": list
        })
    else:
        return render(request, "auctions/details.html", {
            "message": "You successfully closed the auction.",
            "success": True,
            "list": list
        })
    
@login_required
def place(request, list_id):
    list = get_object_or_404(AuctionList, id=list_id)
    newbid = int(request.POST["newBid"])
    if newbid > list.current_bid.bid:
        updateBid = Bid(
            bid= newbid,
            user = request.user
        )
        updateBid.save()
        list.current_bid = updateBid
        list.save()
        return render(request, "auctions/details.html", {
            "message": "You successfully placed a new bid.",
            "success": True,
            "list": list
        })
    else:
        return render(request, "auctions/details.html", {
        "message": "Failed! Make sure you bid more amount than current bid!",
        "success": False,
        "list": list
    })

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
