from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product,Brand,Review
from .serializers import ProductSerializer,BrandSerializer,ReviewSerializer
from rest_framework.exceptions import ValidationError
from .permissions import isAdminOnlyOrGetOnly,IsReviewUserOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ProductListView(generics.ListAPIView,generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes=
    permission_classes=[isAdminOnlyOrGetOnly]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['gender', 'size','brand__name',]
    search_fields = ['^name', 'description','gender', 'size','brand__name']
    ordering_fields = '__all__'
    
class ProductView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    lookup_field='slug'
    queryset=Product.objects.all()
    permission_classes=[isAdminOnlyOrGetOnly]
        
        
class BrandListView(generics.ListAPIView,generics.CreateAPIView):
    serializer_class = BrandSerializer
    # authentication_classes=
    permission_classes=[isAdminOnlyOrGetOnly]
    queryset = Brand.objects.all()
    
class BrandView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BrandSerializer
    queryset=Brand.objects.all()
    permission_classes=[isAdminOnlyOrGetOnly]
        

class ReviewCreate(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise ValidationError('Product you are trying to review does not exist')
        
        review_user=self.request.user
        
        review_queryset = Review.objects.filter(
            product=product, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this product!")
        
        if product.number_rating == 0:
            product.avg_rating = serializer.validated_data['rating']
            
        else:
            product.avg_rating = (
                product.avg_rating + serializer.validated_data['rating'])/2
            
        product.number_rating = product.number_rating + 1
        product.save()
        
        serializer.save(product=product, review_user=review_user)
        
        



class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    
class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Review.objects.filter(product__slug=slug)