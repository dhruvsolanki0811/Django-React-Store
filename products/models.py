from django.db import models
import json
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.'

# class Color(models.Model):
#     color=models.CharField(max_length=100,unique=True)
#     palette=models.CharField(max_length=6,unique=True)
#     def __str__(self) -> str:
#         return self.color
    
SIZE_CHOICES = (('XXS', 'XXS'),
                    ('XS', 'XS'),
                    ('S', 'S'),
                    ('M', 'M'),
                    ('L', 'L'),
                    ('XL', 'XL'),
                    ('XXL', 'XXL'))

GENDER_CHOICES = (('MEN', 'men'),
                    ('WOMEN', 'women'),
                    ('BOYS', 'boys'),
                    ('GIRLS', 'girls'),
                    ('UNISEX', 'unisex'))

CATEGORY_CHOICES = (('jeans', 'jeans'),
                    ('shirts', 'shirts'),
                    ('t-shirts', 't-shirts'),
                    ('shorts', 'shorts'),
                    ('trousers', 'trousers'),
                    ('shoes', 'shoes'),
                    ('traditionals', 'traditionals'),
                    ('sarees','sarees'),
                    ('accessories','accessories'))

# class Size(models.Model):
#     size=models.CharField(choices=SIZE_CHOICES,max_length=100,unique=True)
#     def __str__(self) -> str:
#         return self.size
    
class Brand(models.Model):
    name=models.CharField(max_length=500,unique=True)
    description=models.TextField()
    
    def __str__(self) -> str:
        return self.name
    
    
class Product(models.Model):    
    name=models.CharField(unique=True,max_length=500)
    description=models.TextField()
    image=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    brand= models.ForeignKey(Brand,to_field='name',on_delete=models.CASCADE)
    # color=models.CharField(max_length=500)
    size=models.CharField(choices=SIZE_CHOICES,max_length=100)
    gender=models.CharField(choices=GENDER_CHOICES,max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=100)

    # color=models.ManyToManyField(Color)
    # size=models.ManyToManyField(Size)
    slug=models.SlugField(unique=True)
    
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
        

class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + " | " + self.product.name + " | " + str(self.review_user)