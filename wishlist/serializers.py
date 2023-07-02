from .models import Wishlist,WishlistItems
from rest_framework import serializers


# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Cart
#         field='__all__'
        
class WishlistItemsSerializer(serializers.ModelSerializer):
    wishlist=serializers.IntegerField(source='wishlist.id',read_only=True)

    class Meta:
        model=WishlistItems
        fields='__all__'
        
        