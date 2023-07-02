from django.shortcuts import render
from rest_framework import generics
from .serializers import CartItemSerializer
from .models import CartItems,Cart
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer
from django.forms.models import model_to_dict


class CartItemsListView(generics.ListCreateAPIView):
    serializer_class=CartItemSerializer
    queryset=CartItems.objects.all()
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        
        cart=Cart.objects.get(user=self.request.user)
        if CartItems.objects.filter(items=self.request.data['items'],cart__user=self.request.user.id):
            raise ValidationError('Already on cart')
        
        serializer.save(cart=cart)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError('Eroror')
        
        
        self.perform_create(serializer) 
        user=request.user
    
        filtered_items=[]
        
        user_items=CartItems.objects.filter(cart__user=user.id)
        for item in user_items:
            product=Product.objects.get(slug=item.items.slug)
            product = model_to_dict(product)
            product['quantity']=item.quantity
            filtered_items.append(product)    
        return Response({'cart':filtered_items})
         
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cartQuantityChange(request,*args, **kwargs):
    type=request.data['action']['type']
    product_slug = kwargs.get('slug')
    user=request.user
    cart=Cart.objects.get(user=user)
    req_product=Product.objects.get(slug=product_slug)
    cartItems=CartItems.objects.get(items=req_product,cart=cart)
    if (type=='increment'):
        cartItems.quantity+=1
    if (type=='decrement'):
        cartItems.quantity-=1
    cartItems.save()    
    filtered_items=[]
    user_items=CartItems.objects.filter(cart__user=user.id)
    for item in user_items:
        product=Product.objects.get(slug=item.items.slug)
        product = model_to_dict(product)
        product['quantity']=item.quantity
        filtered_items.append(product)
        
        
    return Response({'cart':filtered_items})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteCartItem(request,*args, **kwargs):
    product_slug = kwargs.get('slug')
    user=request.user
    cart=Cart.objects.get(user=user)
    req_product=Product.objects.get(slug=product_slug)
    cartItems=CartItems.objects.get(items=req_product,cart=cart)
    cartItems.delete()
    
    filtered_items=[]
    user_items=CartItems.objects.filter(cart__user=user.id)
    for item in user_items:
        product=Product.objects.get(slug=item.items.slug)
        product = model_to_dict(product)
        product['quantity']=item.quantity
        filtered_items.append(product)
        
        
    return Response({'cart':filtered_items})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserCart(request,*args, **kwargs):
    product_slug = kwargs.get('slug')
    user=request.user
    
    filtered_items=[]
    user_items=CartItems.objects.filter(cart__user=user.id)
    for item in user_items:
        product=Product.objects.get(slug=item.items.slug)
        product = model_to_dict(product)
        product['quantity']=item.quantity
        filtered_items.append(product)
        
        
    return Response({'cart':filtered_items})