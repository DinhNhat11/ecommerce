from django import forms
from .models import *

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','starting','image','category']
        
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']