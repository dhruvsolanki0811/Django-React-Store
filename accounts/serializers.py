from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):

    # profile = ProfileSerializer()
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    phone_number=serializers.CharField(source='profile.phone_number')
    # date_of_birth=serializers.DateField(source='profile.date_of_birth')
    # city= serializers.CharField(source='profile.city')
    # state= serializers.CharField(source='profile.state')
    # street= serializers.CharField(read_only=True)
    # landmark= serializers.CharField(source='profile.landmark')

    class Meta:
        model = User
        fields=['id','username','email','first_name','password','password2','last_name','phone_number']
        # fields='__all__'
        extra_kwargs = {
            'password' : {'write_only': True},
            'id':{'read_only':True}
        }
        
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'P1 and P2 should be same!'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'],
                       first_name=self.validated_data['first_name'], last_name=self.validated_data['last_name'])
        
        account.set_password(password)
        account.save()
        profile=Profile(user=account,phone_number=self.validated_data['profile']['phone_number'])
        profile.save()
        refresh = RefreshToken.for_user(account)
        access_token = str(refresh.access_token)
        
        return account
    
    
