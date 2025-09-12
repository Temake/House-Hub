from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets,mixins
from drf_spectacular.utils import extend_schema_view, extend_schema
from .permissions import IsUserOwnerOrGetandPostOnly,IsProfileOwnerOrGetOnly
from .serializers import UserSerializer, ProfileSerializer
from .models import Profile

@extend_schema_view(
    list=extend_schema(tags=['Authentication'], summary='List all users'),
    create=extend_schema(tags=['Authentication'], summary='Create a new user'),
    retrieve=extend_schema(tags=['Authentication'], summary='Get user details'),
    update=extend_schema(tags=['Authentication'], summary='Update user'),
    partial_update=extend_schema(tags=['Authentication'], summary='Partially update user'),
    destroy=extend_schema(tags=['Authentication'], summary='Delete user')
)
class UserViewsets(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOwnerOrGetandPostOnly]

@extend_schema_view(
    retrieve=extend_schema(tags=['Authentication'], summary='Get user profile'),
    update=extend_schema(tags=['Authentication'], summary='Update user profile'),
    partial_update=extend_schema(tags=['Authentication'], summary='Partially update user profile')
)
class ProfileViewsets(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    queryset= Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes= [IsProfileOwnerOrGetOnly]