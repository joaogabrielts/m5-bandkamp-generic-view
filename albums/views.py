from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination

from .models import Album
from .serializers import AlbumSerializer


class AlbumView(GenericAPIView, PageNumberPagination):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """
        Obtenção de albums
        """
        albums = self.get_queryset()
        result_page = self.paginate_queryset(albums, request)
        serializer = self.get_serializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Criação de album
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
