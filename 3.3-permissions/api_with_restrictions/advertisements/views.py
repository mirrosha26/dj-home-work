from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from advertisements.models import Advertisement, FavoriteAdvertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.filters import AdvertisementFilter
from rest_framework.pagination import LimitOffsetPagination
from advertisements.permissions import IsOwnerOrReadOnly, IsNotDraftOrIsOwner
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status







class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset =  Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    pagination_class = LimitOffsetPagination


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"] or self.request.user.is_staff:
            return [IsAuthenticated()]

        if self.action in ["update", "partial_update","destroy", 'remove_from_favorites', 'add_to_favorites', 'favorites']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]

        if self.action == 'retrieve':
            return [IsNotDraftOrIsOwner()]
        return []

        
    def list(self, request):
        if request.user.is_authenticated:
            queryset = Advertisement.objects.exclude(
                Q(status='DRAFT') & ~Q(creator=request.user)
            )
        else:
            queryset = self.get_queryset().exclude(status='DRAFT')

        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def favorites(self, request):
        favorite_advertisements = request.user.favorites.all().values_list("advertisement__id", flat=True)
        queryset = Advertisement.objects.filter(id__in=favorite_advertisements)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    


    @action(detail=True, methods=["post"])
    def add_to_favorites(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)
        if request.user != advertisement.creator:
            favorite_advertisement = FavoriteAdvertisement(
                user=request.user,
                advertisement=advertisement
            )
            favorite_advertisement.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Вы не можете добавить своё объявление в избранное."}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=["post"])
    def remove_from_favorites(self, request, pk):
        advertisement = get_object_or_404(Advertisement, pk=pk)
        favorite_advertisement = FavoriteAdvertisement.objects.get(
            user=request.user,
            advertisement=advertisement
        )
        favorite_advertisement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)