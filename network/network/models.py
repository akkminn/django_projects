from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="poster")
    likes = models.ManyToManyField("User", related_name="liked_posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=False)

class Profile(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followings")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")