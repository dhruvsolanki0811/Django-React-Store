from django.urls import path
from . import views
urlpatterns = [
    path('',views.OrderListView.as_view(),name='orderlist-view'),
    path('<int:id>/',views.OrderView.as_view(),name='order-view'),
    # path('pay/', views.start_payment, name="payment"),
    path('payment/success/', views.handle_payment_success, name="payment_success")
]
