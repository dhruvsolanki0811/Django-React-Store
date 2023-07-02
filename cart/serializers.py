from .models import Cart,CartItems
from rest_framework import serializers


# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Cart
#         field='__all__'
        
class CartItemSerializer(serializers.ModelSerializer):
    cart=serializers.IntegerField(source='cart.id',read_only=True)
    
    class Meta:
        model=CartItems
        fields='__all__'
        
        