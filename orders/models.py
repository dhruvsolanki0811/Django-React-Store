from django.db import models
from products.models import Product
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    total=models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address=models.TextField()
    email= models.EmailField()
    phone_number = models.CharField(max_length=12)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
    order_payment_id = models.CharField(max_length=100,null=True)
    ordered_user= models.ForeignKey(User, on_delete=models.CASCADE)
    
    
class Purchases(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,to_field='name',related_name='product_name')
    quantity=models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='purchases',to_field='order_id') 
    size=models.CharField(max_length=100)
    price= models.DecimalField(max_digits=10, decimal_places=2)
