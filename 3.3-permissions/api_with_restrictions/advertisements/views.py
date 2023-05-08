from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.filters import AdvertisementFilter
from rest_framework.pagination import LimitOffsetPagination
from advertisements.permissions import IsOwnerOrReadOnly



class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset =  Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    pagination_class = LimitOffsetPagination


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update","destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []
