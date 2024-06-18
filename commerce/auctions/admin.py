from django.contrib import admin

from .models import AuctionList, Bid, Category, Comment

admin.site.register(AuctionList)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)