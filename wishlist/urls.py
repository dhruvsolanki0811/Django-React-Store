from . import views
from django.urls import path
urlpatterns = [
    path('create/',views.WishlistItemsListView.as_view(),name='cartlist-view'),
    path('delete/<slug:slug>/',views.deleteWishlistItem,name='orderlist-view'),
    path('',views.getUserWishlist,name='orderlist-view'),

]