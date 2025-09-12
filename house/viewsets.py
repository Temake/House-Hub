from rest_framework import viewsets,status,filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import house
from django.contrib.auth.models import User
from .serializers import HouseAppSerializers
from .permissions import IsManagerorNone

@extend_schema_view(
    list=extend_schema(tags=['Houses'], summary='List all houses'),
    create=extend_schema(tags=['Houses'], summary='Create a new house'),
    retrieve=extend_schema(tags=['Houses'], summary='Get house details'),
    update=extend_schema(tags=['Houses'], summary='Update house'),
    partial_update=extend_schema(tags=['Houses'], summary='Partially update house'),
    destroy=extend_schema(tags=['Houses'], summary='Delete house'),
    join=extend_schema(tags=['Houses'], summary='Join a house'),
    leave=extend_schema(tags=['Houses'], summary='Leave a house'),
    remove_member=extend_schema(tags=['Houses'], summary='Remove member from house')
)
class HouseViewSet(viewsets.ModelViewSet):
    queryset = house.objects.all()
    serializer_class = HouseAppSerializers
    permission_classes=[IsManagerorNone]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['name','description']
    filterset_fields=['members',]
    
    @action(detail=True, methods=['post','get'],name='join',permission_classes=[])
    def join(self, request, pk=None):
        try:
             house = self.get_object()
             user_profile = request.user.profile
             if user_profile.house==None:
                user_profile.house=house
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
               
             elif request.user.profile in house.members.all():
                return Response({'status': 'already a member'}, status=status.HTTP_400_BAD_REQUEST)
             else:
                return Response({'status': 'already a member in another house'}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(methods=['post','get'], detail=True,name='leave',permission_classes=[])
    def leave(self, request, pk=None):
        try:
            house = self.get_object()
            profile = request.user.profile

            if not profile.house or profile.house != house:
                return Response({'error': 'You are not a member of this house'}, status=status.HTTP_400_BAD_REQUEST)

            house.members.remove(profile)
            profile.house = None
            profile.save()

            return Response({'message': 'You have left the house'}, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['post',], name='remove_member')
    def remove_member(self, request, pk=None):
        try:
            house = self.get_object()
            profile_id = request.data.get('profile_id')

            if profile_id:
                profile = User.objects.get(id=profile_id).profile
                if profile in house.members.all() and request.user.profile == house.manager:
                    house.members.remove(profile)
                    house.save()
                    return Response({'message': 'Member removed'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'You are not a manager or the member is not in the house'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Profile ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  
