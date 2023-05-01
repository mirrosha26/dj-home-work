from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination


class ConstLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 100


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    pagination_class = ConstLimitOffsetPagination
    filter_backends = [ OrderingFilter, SearchFilter]
    ordering_fields = ['id', 'title']
    search_fields = ['title', 'description']



class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    pagination_class = ConstLimitOffsetPagination
    filter_backends = [ OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ['id', 'address']
    filterset_fields = ['products']
    search_fields = ['products__title', 'products__description']

