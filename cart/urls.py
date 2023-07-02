from . import views
from django.urls import path
urlpatterns = [
    path('create/',views.CartItemsListView.as_view(),name='cartlist-view'),
    path('change/<slug:slug>/',views.cartQuantityChange,name='orderlist-view'),
    path('delete/<slug:slug>/',views.deleteCartItem,name='orderlist-view'),
    path('',views.getUserCart,name='orderlist-view'),

]