from django.contrib import admin
from .models import *
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id","title","description","user","category")
    filter_horizontal = ("watchlist",)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id","category")


admin.site.register(Listing,ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Categories,CategoriesAdmin)
admin.site.register(User)
