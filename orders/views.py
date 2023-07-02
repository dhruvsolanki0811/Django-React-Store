from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Purchases,Order
from .serializers import PurchaseSerializer,OrderSerializer
from rest_framework.exceptions import ValidationError


#Environment variable configuration 
import json
import environ
import os
import razorpay
env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, '.env')
environ.Env.read_env(env_file=env_path)


# Create your views here.

class OrderListView(generics.ListAPIView,generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # authentication_classes=
    permission_classes=[IsAuthenticated]
    
class OrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset=Order.objects.all()
    lookup_field='id'
    permission_classes=[IsAuthenticated]
        


# @api_view(['GET'])
# def start_payment(request):
#     # request.data is coming from frontend
#     # amount = request.data['amount']
#     # name = request.data['name']   
#     # env = environ.Env()
#     # env.read_env(env_file='.env')
#     return Response({"okay":1})




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_payment_success(request):
    res = json.loads(request.data["response"])

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    
    if check is None:
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()
    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)


