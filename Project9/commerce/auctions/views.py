from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comments

login_url = '/login'

def index(request):
    Categories = list(set(
        [listing.category.lower().capitalize() for listing in Listing.objects.filter(closed=False)]
        ))
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(closed=False),
        "categories": Categories,
        "watchlist": False
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

@login_required(login_url=login_url)
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        starting_bid = request.POST["starting_bid"]
        description = request.POST["description"]
        category = request.POST["category"]
        image = request.POST["image"]
        user = User.objects.get(username=request.user.username)
        new_listing = Listing(title=title, description=description, starting_bid=starting_bid,
                url=image, category=category, listed_by=user)
        new_listing.save()
        new_bid = Bid(listed_item=new_listing)
        new_bid.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")
    
def filter(request):
    if request.method == "POST":
        Categories = list(set(
            [listing.category.lower().capitalize() for listing in Listing.objects.filter(closed=False)])
        )
        category = request.POST['filter']
        if category == 'all':
            listings = Listing.objects.filter(closed=False)
        elif category == 'closed':
            listings = Listing.objects.filter(closed=True)
        else:
            listings = Listing.objects.filter(category=category, closed=False)
        return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": Categories,
            "watchlist": False
        })
    
def listing(request, id):
    Item = Listing.objects.get(listing_id=id)
    if Item.listed_by == request.user:
        owner = True
    else:
        owner = False
    if request.user in Item.watchlist.all():
        message = "Remove From Watchlist"
    else:
        message = "Add To Watchlist"
    bidder = Item.bids.get(listed_item=Item).bidder
    if bidder == None:
        bidder = ''
    else:
        bidder = bidder.username
    comments = Comments.objects.filter(listed_item=Item)
    return render(request, "auctions/item.html", {
        "listing": Item,
        "message": message,
        "owner": owner,
        "highest_bid": Item.bids.get(listed_item=Item).highest_bid,
        "bidder": bidder,
        "comments": comments
    })

@login_required(login_url=login_url)
def watchlist(request, id):
    Item = Listing.objects.get(listing_id=id)
    if request.user in Item.watchlist.all():
        Item.watchlist.remove(request.user)
    else:
        Item.watchlist.add(request.user)
    return redirect("listing", id=Item.listing_id)

@login_required(login_url=login_url)
def watchlist_page(request):
    watch = request.user.watchlisted.all()
    Categories = []
    return render(request, "auctions/index.html", {
        "listings": watch,
        "categories": Categories,
        "watchlist": True
    })

@login_required(login_url=login_url)
def make_bid(request, id):
    if request.method == "POST":
        Item = Listing.objects.get(listing_id=id)
        CurrentBid = Bid.objects.get(listed_item=Item)
        highest_bid = CurrentBid.highest_bid
        bid = float(request.POST['bid'])
        if bid > float(highest_bid) and bid >= float(Item.starting_bid):
            CurrentBid.highest_bid = bid
            CurrentBid.bidder = request.user
            CurrentBid.save()
            return redirect("listing", id=Item.listing_id)
        else:
            return HttpResponse("Error! The bid has to be greater than the current highest bid or starting bid!")

@login_required(login_url=login_url)
def close(request, id):
    if request.method == "POST":
        Item = Listing.objects.get(listing_id=id)
        Item.closed = True
        Item.save()
        return redirect("listing", id=Item.listing_id)

@login_required(login_url=login_url)
def comment(request, id):
    if request.method == "POST":
        comment = request.POST['comment']
        Item = Listing.objects.get(listing_id=id)
        user = request.user
        NewComment = Comments(listed_item=Item, user=user, comment=comment)
        NewComment.save()
        return redirect("listing", id=Item.listing_id)

def reply(request, id):
    comment = Comments.objects.get(comment_id=id)
    reply = request.POST['reply']
    comment.reply = reply
    comment.replied = True
    Item = comment.listed_item
    comment.save()
    return redirect("listing", id=Item.listing_id)