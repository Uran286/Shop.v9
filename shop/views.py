from datetime import timedelta

from django.http import HttpResponseRedirect
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import serializers
from rest_framework import generics, permissions
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView


from .models import Product, Category, Choosen
from .serializers import ProductSerializer, CategoryApiSerializer, UserSerializer, ChoosenAPISerializer



User = get_user_model()


class MyPaginationClass(PageNumberPagination):

    def get_paginated_response(self, data):
        for i in range(self.page_size):
            description = data[i]['description']
            if len(description) > 10:
                data[i]['description'] = description[:10] + '...'
        return super().get_paginated_response(data=data)


class ProductListApiView(generics.ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    """  search  """

    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('id', 'title', 'price',)

    """ filter by price """

    def get_queryset(self):
        price = self.request.query_params.get('price')
        queryset = super().get_queryset()
        if price:
            price_from, price_to = price.split('-')
            queryset = queryset.filter(
                price__gt=price_from,
                price__lt=price_to
            )
        return queryset


class CategoryApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryApiSerializer



class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ChoosenListApiView(generics.ListCreateAPIView):
    serializer_class = ChoosenAPISerializer

    def get_queryset(self):
        queryset = Choosen.objects.all()
        return Choosen.objects.filter(user=self.request.user.id)

    def post(self, request, *args, **kwargs):
        if len(request.data.keys()) == 1 and request.data.get('product'):
            user = request.user.id
            product = request.data['product']
            favorites = Choosen.objects.filter(product=product, user=user.id)
            if favorites:
                raise serializers.ValidationError('Product in WishList')
            request.data['user'] = request.user.id

        else:
            raise serializers.ValidationError('Error')
            pass
        return self.create(request, *args, **kwargs)



class ChoosenAdd(APIView):
    
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        user = request.user
        url = request.build_absolute_uri()
        if Choosen.objects.filter(user=user.id, product=pk):
            raise serializers.ValidationError('OK')
        new_favorite = Choosen.objects.create(user=user, product=product)
        return HttpResponseRedirect(redirect_to=url)


class ChoosenDelete(APIView):

    def get(self, request, pk):
        user = request.user
        print(user)
        product = Product.objects.get(pk=pk)

        favor = Choosen.objects.filter(user=user.id, product=pk)
        print(favor)
        if favor:
            favor.delete()
            raise serializers.ValidationError('Your product deleted!')
        raise serializers.ValidationError('Product not found!')




