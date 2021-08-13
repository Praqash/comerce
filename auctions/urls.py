from django.urls import path
from .views import ALListView, ALDetailView, ALCreateView , ALDeleteView
from . import views

urlpatterns = [
    path("", ALListView.as_view(), name="index"),

    path("listing", views.com, name="com"),
    path("bidder", views.bidder, name="bidder"),
    path("listing/<int:pk>", ALDetailView.as_view(), name="al_detail"),
    path("listing/new", ALCreateView.as_view(), name="create"),
    path("listing/<int:pk>/delete", ALDeleteView.as_view(), name="al-delete"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.cat, name="cat"),
    path("watchlist/<int:id>", views.watchlist, name="watchlist"),
    path("watchlist", views.watch_list, name="watch_list"),
    path("closed_auctions", views.closed_auctions, name="closed_auctions"),
    path("delete", views.delete, name="delete"),
   
    
  
]
