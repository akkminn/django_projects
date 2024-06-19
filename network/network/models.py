from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="poster")
    likes = models.ManyToManyField("User", related_name="liked_posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=False)

    def __str__(self):
        return f"Post by {self.user.username} at {self.timestamp}"

class Profile(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followings")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    content = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id} at {self.timestamp}"