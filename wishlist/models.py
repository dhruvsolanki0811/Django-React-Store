from django.db import models

# Create your models here.
from django.db import models
from products.models import Product
from django.contrib.auth.models import User
# Create your models here.
class Wishlist(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return 'Wishlist of '+str(self.user)
    
    
class WishlistItems(models.Model):
    items=models.ForeignKey(Product,on_delete=models.CASCADE,to_field='slug',related_name='wishitems')
    wishlist=models.ForeignKey(Wishlist,on_delete=models.CASCADE,related_name='wishlist') 

    def __str__(self) -> str:
        return str(self.wishlist)+ '|' +str(self.items.slug) 