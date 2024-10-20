from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path("listings/<int:listing_id>",views.listing,name="listing"),
    path("categories",views.categories,name="categories"),
    path("onecategory/<int:category_id>",views.onecategory,name="onecategory"),
    path("listings/<int:listing_id>/comment",views.comment,name="comment"),
    path("listings/<int:listing_id>/bid",views.bid,name="bid"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("listings/<int:listing_id>/closeBid",views.closeBid,name="closeBid"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
