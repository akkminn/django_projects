from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return self.name
    
class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    
    def __str__(self):
        return f"{self.bid}; User: {self.user}"
    

class AuctionList(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    imageURL = models.URLField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="list_owner")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='category')
    start_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="start_bid")
    time = models.DateTimeField(auto_now_add=True)  # Auto add current datetime
    watchlists = models.ManyToManyField(User, blank=True, related_name='watchlist')
    
    def __str__(self):
        watchlist_count = self.watchlists.count()
        return f"{self.title}; Description: {self.description}; Owner: {self.owner}; Category: {self.category}; Starting Bid: {self.start_bid}; Is active: {self.is_active}; Watchlist Count: {watchlist_count}"
    
    class Meta:
        ordering = ['-is_active', 'title']
        verbose_name_plural = "Auction Listings"
    

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    time = models.DateTimeField(auto_now_add=True)  # Auto add current datetime
    auction_list = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="auction_comment")
    
    def __str__(self):
        return f"Commenter: {self.user}; Comment: {self.comment}; Date: {self.time}; Auction List: {self.auction_list.title}"
    
    class Meta:
        ordering = ['-time']
        verbose_name_plural = "Comments"