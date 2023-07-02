from django.urls import path
from . import views
urlpatterns = [
    path('',views.ProductListView.as_view(),name='productlist-view'),
    path('<slug:slug>/',views.ProductView.as_view(),name='productlist-view'),
    path('brands/',views.BrandListView.as_view(),name='brandlist-view'),
    path('brands/<int:id>/',views.BrandView.as_view(),name='brandlist-view'),
    
    path('<slug:slug>/reviews/create/', views.ReviewCreate.as_view(), name='review-create'),
    path('<slug:slug>/reviews/', views.ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),
]
