from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

    
# class PublicUserRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     phone = serializers.CharField(
#         validators=[UniqueValidator(queryset=CustomUser.objects.all())]
#     )

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password', "phone", "role"] 

#     def validate_role(self, value):
#         if value not in ["customer", "vendor"]:
#             raise serializers.ValidationError("Invalid role selection.")
#         return value


#     def create(self, validated_data):
#         role = validated_data.pop("role")

#         user = CustomUser.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#             phone=validated_data["phone"],
#             role=role 
#         )
#         return user

class PublicUserRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    phone = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "phone", "role"]

    def validate_role(self, value):
        if value not in ["customer", "vendor"]:
            raise serializers.ValidationError(
                "Role must be customer or vendor"
            )
        return value

    def create(self, validated_data):

        role = validated_data.pop("role", "customer")

        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data["phone"],
            role=role,
        )

        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})





class AdminManagedUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'role']

    def validate_role(self, value):
        if value != 'admin':
            raise serializers.ValidationError("Admins only")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
