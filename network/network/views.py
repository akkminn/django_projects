from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Profile


def index(request):
    allPosts = Post.objects.all().order_by("-timestamp")

    # pignation
    paginator = Paginator(allPosts, 10)
    pageNum = request.GET.get("page")
    pages = paginator.get_page(pageNum)

    return render(request, "network/index.html", {"posts": allPosts, "pages": pages})


@login_required
def following(request):
    currentUser = User.objects.get(pk=request.user.id)
    myfollowing = Profile.objects.filter(follower=currentUser).values("following_id")
    allPosts = Post.objects.filter(user__in=myfollowing).order_by("-timestamp")

    # pignation
    paginator = Paginator(allPosts, 10)
    pageNum = request.GET.get("page")
    pages = paginator.get_page(pageNum)

    return render(request, "network/following.html", {"posts": pages})


@csrf_exempt
@login_required
def postedit(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    data = json.loads(request.body)
    post_id = data.get("post_id", "")
    post = Post.objects.get(id=post_id)

    content = data.get("content", "")
    toggle_like = data.get("toggle_like", "")
    if content:
        if request.user != post.user:
            return JsonResponse({"error": "Can only edit your own posts"})

        post.content = content

    if toggle_like:
        if request.user in post.likes.all():
            post.likes.remove(request.user)

        else:
            post.likes.add(request.user)
    post.save()
    return JsonResponse(
        {"message": "Post edited successfully", "likes_num": str(post.likes.count())},
        status=201,
    )


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    allPosts = Post.objects.filter(user=user).order_by("-timestamp")

    followings = Profile.objects.filter(follower=user).count()
    followers = Profile.objects.filter(following=user).count()

    if not request.user.is_authenticated:
        # pignation
        paginator = Paginator(allPosts, 10)
        pageNum = request.GET.get("page")
        pages = paginator.get_page(pageNum)

        return render(
            request,
            "network/profile.html",
            {
                "user": request.user,
                "user_profile": user,
                "followers": followers,
                "followings": followings,
                "posts": pages,
            },
        )

    else:
        if (
            Profile.objects.filter(
                following=user, follower=User.objects.get(pk=request.user.id)
            ).count()
            == 0
        ):
            isfollowing = False
        else:
            isfollowing = True

        # pignation
        paginator = Paginator(allPosts, 10)
        pageNum = request.GET.get("page")
        pages = paginator.get_page(pageNum)

        return render(
            request,
            "network/profile.html",
            {
                "user": request.user,
                "user_profile": user,
                "followers": followers,
                "followings": followings,
                "posts": pages,
                "isfollowing": isfollowing,
            },
        )


def follow(request):
    userfollow = request.POST["userfollow"]
    currentUser = User.objects.get(pk=request.user.id)
    Data = User.objects.get(username=userfollow)

    f = Profile(follower=currentUser, following=Data)
    f.save()
    user_id = Data.id
    return HttpResponseRedirect(reverse(profile, kwargs={"user_id": user_id}))


def unfollow(request):
    userfollow = request.POST["userfollow"]
    currentUser = User.objects.get(pk=request.user.id)
    Data = User.objects.get(username=userfollow)

    f = Profile.objects.get(following=Data, follower=currentUser)
    f.delete()
    user_id = Data.id
    return HttpResponseRedirect(reverse(profile, kwargs={"user_id": user_id}))


@login_required
def newpost(request):
    if request.method == "POST":
        # Get contents of post
        user = request.user
        content = request.POST["newpost"]
        timestamp = datetime.now()

        # Create new post
        post = Post(user=user, content=content, timestamp=timestamp)
        post.save()

        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/index.html")


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
