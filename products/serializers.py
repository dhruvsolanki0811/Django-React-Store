from rest_framework import serializers
from .models import Product,Brand,Review
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault
from django.contrib.auth.models import User


# class ColorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Color
#         # fields='__all__'
#         fields=['color','palette']
    
    
# class SizeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Size
#         fields=['size']
    
    
class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('product',)
        # fields = "__all__"
        
    
class ProductSerializer(serializers.ModelSerializer):
    # brand = BrandSerializer() 
   
    # color = ColorSerializer(many=True,)
    # size = SizeSerializer(many=True)
    brand_name = serializers.CharField(source='brand.name')
    # size = serializers.CharField(source='size.size',many=True)
    # color = serializers.(source='color.color',many=True)
    # palette = serializers.CharField(source='color.palette',many=True)
    # color_given = serializers.ListField(child=serializers.DictField(), write_only=True)
    # size_given= serializers.ListField(child=serializers.DictField(), write_only=True)
    class Meta:
        model = Product
        exclude=['brand','id','created_at','updated_at','created_by']
        extra_fields=['brand_name']
        extra_kwargs = {
            'slug' : {'read_only': True},            
        }
    
    def create(self, validated_data):
  
        brand_name=validated_data['brand']['name']
        
        try:
            brand= Brand.objects.get(name=brand_name)
        except Brand.DoesNotExist:
            raise ValidationError('Brand doesnt exist')
        
        # available_color=[]
        # for requested_color in validated_data['color_given']:
        #     color_name=requested_color['color']
        #     palette=requested_color['palette']
        #     if not Color.objects.filter(color=color_name).exists():
        #         color=Color.objects.create(color=color_name,palette=palette)
        #     else:
        #         color=Color.objects.filter(color=color_name)[0]
                
        #     available_color.append(color)
            
        # available_size=[]
        # for requested_size in validated_data['size_given']:    
        #     size_name=requested_size['size']
        #     if not Size.objects.filter(size=size_name).exists():
        #         size=Size.objects.create(size=size_name)
        #     else:
        #         size=Size.objects.filter(size=size_name)[0]
                
        #     available_size.append(size)
        validated_data['created_by_id'] = self.context['request'].user 
        user=User.objects.filter(username=validated_data['created_by_id'])[0]
        try:
            product=Product.objects.create(brand=brand,name=validated_data['name'],
                                           category=validated_data['category'],
                                           size=validated_data['size'],
                                           gender=validated_data['gender'],
                                           description=validated_data['description'],
                                           image=validated_data['image'],
                                           price=validated_data['price'],
                                           created_by=user,
                                           )
            product.save()
            
        except Exception as ex:
            raise ValidationError(ex)
        # return 
        return validated_data
            
            
        


        


class BrandSerializer(serializers.ModelSerializer):
    products=ProductSerializer(many=True)
    class Meta:
        model = Brand
        fields='__all__'        
        # exclude=['id']
    