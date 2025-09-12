from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile
 
class ProfileSerializer(serializers.ModelSerializer):
    
    user=serializers.HyperlinkedRelatedField(many=False,read_only=True,view_name='user-detail')

    class Meta:
        model= Profile
        fields=['url','user','img','id']
      
class UserSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True,required=False)
    username= serializers.CharField(read_only=True)
    old_password= serializers.CharField(write_only=True,required=False)
    profile= ProfileSerializer(read_only=True)
    

    

    def create(self,validated_data):
        if User.objects.filter(email=validated_data.get('email')).exists():
            raise serializers.ValidationError({'info':'Email Already exists'})
        password= validated_data.pop('password')
        user= User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        request_method= self.context.get('request').method
        old_password= data.get('old_password',None)
        password= data.get('password',None)
        if request_method == 'POST':
                raise serializers.ValidationError({'info': 'Password cannot be empty'})
        elif request_method == 'PUT' or request_method == 'PATCH':
           
            if password != None and old_password == None:
                raise serializers.ValidationError({'info': 'Old password cannot be empty'})
        return data
        
    def update(self,instance,validated_data):
        user = instance
        if 'password' in validated_data:
            password = validated_data.pop('password', None)
            old_password = validated_data.pop('old_password', None)

            if password and old_password:
                if user.check_password(old_password):
                    user.set_password(password)
                else:
                    raise serializers.ValidationError({'old_password': 'Old password is not correct'})
            user.save()
        return super(UserSerializer,self).update(instance,validated_data)
        

    class Meta:
        model = User
        fields = ['url','id','username','email','first_name','last_name','email','password','old_password','profile']
