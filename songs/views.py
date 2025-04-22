from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Song
from .serializers import SongSerializer
from albums.models import Album


class SongView(GenericAPIView, PageNumberPagination):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        """
        Obtenção de músicas
        """
        songs = self.get_queryset().filter(album_id=pk)
        result_page = self.paginate_queryset(songs, request)
        serializer = self.get_serializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, pk):
        """
        Criação de música
        """
        album = get_object_or_404(Album, pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(album=album)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
