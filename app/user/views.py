from django.contrib.auth import get_user_model, authenticate

from rest_framework import generics, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings

from user.serializers import UserSerializer, UserSerializerWithToken

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RegisterUsersView(generics.CreateAPIView):
    """Create a new user in the system"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(generics.ListCreateAPIView):
    """Login existing users"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = authenticate(request, email=email, password=password)

        if user:
            serializer = UserSerializerWithToken(data={
                'token': jwt_encode_handler(jwt_payload_handler(user))
            })
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """REtrieve and return authenticated user"""
        return self.request.user
