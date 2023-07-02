from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import ValidationError
# Create your views here.
class CreateUserListView(generics.ListAPIView,generics.CreateAPIView    ):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError('Eroror')
        
        # Perform any custom processing or additional logic here
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Customize the response data as needed
        
        # User.objects.get(username=request.data['username'])
        user=User.objects.get(username=request.data['username'])
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response_data = {
            'status': 'success',
            'message': 'Custom success message',
            'data': serializer.data,
            'access':access_token,
            'refresh':str(refresh)
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)        

@api_view(['POST'])
def login(request):
    email = request.data.get('email', None)
    password = request.data.get('password', None)

    if not email or not password:
        return Response({'error': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({"refresh":str(refresh),'access': access_token}, status=status.HTTP_200_OK)