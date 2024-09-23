from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return self.username

class Listing(models.Model):
    listing_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    starting_bid = models.FloatField()
    url = models.CharField(max_length=128, blank=True)
    category = models.CharField(max_length=32, blank=True)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlisted")
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} listed by {self.listed_by.username} at {self.starting_bid}"

class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    listed_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    highest_bid = models.FloatField(default=0.0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="user_bids", blank=True, null=True)

class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    listed_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", auto_created=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented")
    comment = models.CharField(max_length=256)
    replied = models.BooleanField(default=False)
    reply = models.CharField(max_length=256, null=True, blank=True)