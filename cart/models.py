from django.db import models
from products.models import Product
from django.contrib.auth.models import User
# Create your models here.
class Cart(models.Model):
    user=  models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return 'Cart of '+str(self.user)
    
    
class CartItems(models.Model):
    items=models.ForeignKey(Product,on_delete=models.CASCADE,to_field='slug',related_name='items')
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart') 
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.cart)+ '|' +str(self.items.slug) +'|'+ str(self.quantity) 