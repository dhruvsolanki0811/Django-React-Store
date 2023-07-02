from django.shortcuts import render
from rest_framework import generics
from .serializers import WishlistItemsSerializer
from .models import Wishlist,WishlistItems
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer
from django.forms.models import model_to_dict


class WishlistItemsListView(generics.ListCreateAPIView):
    serializer_class=WishlistItemsSerializer
    queryset=WishlistItems.objects.all()
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        
        wishlist=Wishlist.objects.get(user=self.request.user)
        if WishlistItems.objects.filter(items=self.request.data['items'],wishlist__user=self.request.user.id):
            raise ValidationError('already on whishlist')
        
        serializer.save(wishlist=wishlist)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError('Eroror')
        self.perform_create(serializer) 
        user=request.user
    
        filtered_items=[]
        user_items=WishlistItems.objects.filter(wishlist__user=user.id)
        for item in user_items:
            product=Product.objects.get(slug=item.items.slug)
            product = model_to_dict(product)
            filtered_items.append(product)    
        return Response({'wishlist':filtered_items})
         
        
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteWishlistItem(request,*args, **kwargs):
    product_slug = kwargs.get('slug')
    user=request.user
    wishlist=Wishlist.objects.get(user=user)
    req_product=Product.objects.get(slug=product_slug)
    cartItems=WishlistItems.objects.get(items=req_product,wishlist=wishlist)
    cartItems.delete()
    
    filtered_items=[]
    user_items=WishlistItems.objects.filter(wishlist__user=user.id)
    for item in user_items:
        product=Product.objects.get(slug=item.items.slug)
        product = model_to_dict(product)
        filtered_items.append(product)
        
        
    return Response({'wishlist':filtered_items})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserWishlist(request,*args, **kwargs):
    user=request.user
    
    filtered_items=[]
    user_items=WishlistItems.objects.filter(wishlist__user=user.id)
    for item in user_items:
        product=Product.objects.get(slug=item.items.slug)
        product = model_to_dict(product)
        filtered_items.append(product)
        
        
    return Response({'wishlist':filtered_items})