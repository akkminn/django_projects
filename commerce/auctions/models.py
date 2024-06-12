from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return self.name
    

class AuctionList(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    imageURL = models.TextField()
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="list_owner")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='category')
    start_bid = models.IntegerField()
    watchlists = models.ManyToManyField(User, blank=True, related_name='watchlist')
    
    def __str__(self):
        watchlist_count = self.watchlists.count()
        return f"{self.title}; Description: {self.description}; Owner: {self.owner}; Category: {self.category}; Starting Bid: {self.start_bid}; Is active: {self.is_active}; Watchlist Count: {watchlist_count}"
    
    
class Bid(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    bid_list = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name='bid_list')
    
    def __str__(self):
        return f"{self.bid} by {self.user} for {self.bid_list.title}"
    
     
class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    time = models.DateTimeField("date")
    auction_list = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="auction_list")
    
    def __str__(self):
        return f"Commenter: {self.user}; Comment: {self.comment}; Date: {self.time}; Auction List: {self.auction_list.title}"
