from rest_framework import serializers
from .models import Order,Purchases
from products.models import Product
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User 
#Environment variable configuration 
import environ
import os
import razorpay
env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, '.env')
environ.Env.read_env(env_file=env_path)



class PurchaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Purchases
        # fields='__all__'
        exclude=['id']
        extra_kwargs = {
            'order_id' : {'read_only': True},
            'price' : {'read_only': True},
        }
class OrderSerializer(serializers.ModelSerializer):
    purchases=PurchaseSerializer(many=True)
    class Meta:
        model=Order
        # fields='__all__'
        exclude=['id']
        extra_fields=['purchases']
        extra_kwargs = {
            # 'total' : {'read_only': True},
            'order_payment_id':{'read_only':True},
            'ordered_user':{'read_only':True}
        }
    
    def create(self, validated_data):
        shipping_address=validated_data['shipping_address']
        email=validated_data['email']
        phone_number=validated_data['phone_number']
        total=validated_data['total']
        
        
        
        for purchase in validated_data['purchases']:
            product=Product.objects.filter(name=purchase['product'],size=purchase['size'])              
            if not product.exists():
                raise ValidationError('Product listed in the purchase list maybe not be in the stocks currently')
        

        
        client = razorpay.Client(auth=(str(env('PUBLIC_KEY')), str(env('SECRET_KEY'))))
        payment = client.order.create({"amount": int(total) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})
            
        ordered_user=self.context['request'].user       
        req_order= Order.objects.create(ordered_user=ordered_user,
                                        order_payment_id=payment['id']
                                        ,shipping_address=shipping_address,email=email,phone_number=phone_number,total=total)
        
        price=0
        
        for purchase in validated_data['purchases']:
           
            product=Product.objects.filter(name=purchase['product'])[0]
            price+=product.price*purchase['quantity']
            purchase_check=Purchases(price=price,product=product,quantity=purchase['quantity'],size=purchase['size'],order_id=req_order )
            purchase_check.save()
        

        req_order.save()
        return req_order    
            