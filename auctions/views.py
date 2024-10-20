from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *


def index(request):
    active = Listing.objects.filter(is_close=False)
    return render(request, "auctions/index.html",{
        "listings":active
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

@login_required    
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST,request.FILES)
        if form.is_valid():        
            newlisting = form.save(commit=False)
            newlisting.user = request.user
            category_id = int(request.POST["category"])
            category = Categories.objects.get(pk=category_id)
            newlisting.category = category
            if request.POST["newcategory"]:
                newcategory = Categories(category=request.POST["newcategory"])
                newcategory.save()
                newlisting.category = newcategory
            newlisting.save()
            return HttpResponseRedirect(reverse("listing",args=(newlisting.id,)))
        else:
            return render(request,"auctions/create.html",{
                "form":form
            })
    else:
        return render(request,"auctions/create.html",{
            "form": ListingForm(),
            "categories":Categories.objects.all()
        })     
        
        
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.comments.all()
    bidlast = listing.listingbids.last()
    added = False
    closePermit = False
    won = False
    if request.user.is_authenticated:
        if request.user in listing.watchlist.all():
            added = True
        if listing.user == request.user:
            closePermit = True
        if listing.is_close:
            wonbid = listing.listingbids.last()
            if wonbid:
                won = f"This auction listing is won by {wonbid.user}"
            else:
                won = "Nobody bid this auction."
    if request.method == "POST":
        if "addwatchlist" in request.POST:
            listing.watchlist.add(request.user)
            added = True
        elif "removewatchlist" in request.POST:
            listing.watchlist.remove(request.user)
            added = False
            
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "added": added,
        "formComment":CommentForm(),
        "closePermit":closePermit,
        "won":won,
        "bidlast": bidlast,
        "comments": comments,
        'formBid':BidForm()
    })
    
def closeBid(request,listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)  
        listing.is_close = True
        listing.save()
        return HttpResponseRedirect(reverse("listing",args=[listing_id]))
        
        

def categories(request):
    if request.user.is_authenticated:
        return render(request,"auctions/categories.html",{
            "categories": Categories.objects.all()
        })
def onecategory(request,category_id):
    category = Categories.objects.get(pk=int(category_id))
    return render(request,"auctions/index.html",{
        "listings": category.categories.all()  
    })
    
def comment(request,listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(listing_id))
        comments = listing.comments.all()
        bidlast = listing.listingbids.last()
        form = CommentForm(request.POST)
        if form.is_valid():
            newcomment = form.save(commit=False)
            newcomment.user = request.user
            newcomment.listing = listing
            newcomment.save()
            return HttpResponseRedirect(reverse('listing',args=[listing_id]))
        return render(request,"auctions/listing.html",{
            "listing":listing,
            "formComment":form,
            "bidlast": bidlast,
            "formBid":BidForm(),
            "comments":comments
        })
        
def bid(request,listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(listing_id))
        comments = listing.comments.all()
        bidlast = listing.listingbids.last()
        form = BidForm(request.POST)
        if form.is_valid():
            price = request.POST['price']
            if int(price) >= listing.starting:
                if bidlast:
                    int(price) > bidlast.price
                newBid = form.save(commit = False)
                newBid.user = request.user
                newBid.listing = listing
                newBid.save()
                return HttpResponseRedirect(reverse("listing",args=[listing_id]))
            else:
                return render(request,"auctions/listing.html",{
                    "listing":listing,
                    "formBid":form,
                    "bidlast": bidlast,
                    "error":"Bid must be as large as starting bid, and must be greater than any other bids that have been placed.",
                    "formComment":CommentForm(),
                    "comments":comments
                })
        return render(request,"auctions/listing.html",{
            "listing":listing,
            "formBid":form,
            "bidlast": bidlast,
            "formComment":CommentForm(),
            "comments":comments
        })
    return HttpResponse("Unexpected error occurred", status=500)
            
def watchlist(request):
    return render(request,"auctions/index.html",{
        "listings":request.user.watchlist.all()
    })
