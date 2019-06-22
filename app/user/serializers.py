from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return data"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user and set password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ('token', 'email', 'password')

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


# class AuthTokenSerializer(serializers.Serializer):
#     """Serializer for the user authentication object"""
#     email = serializers.CharField()
#     password = serializers.CharField(
#         style={'input_type': 'password'},
#         trim_whitespace=False
#     )

#     def validate(self, attrs):
#         """Validate and authenticate user"""
#         email = attrs.get('email')
#         password = attrs.get('password')

#         user = authenticate(
#             request=self.context.get('request'),
#             username=email,
#             password=password
#         )
#         if not user:
#             msg = _('Unable to authenticate with provided credentials')
#             raise serializers.ValidationError(msg, code='authentication')

#         attrs['user'] = user
#         return attrs
