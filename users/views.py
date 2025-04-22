from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404

class UserDetailView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    lookup_url_kwarg = "pk"

    def get(self, request: Request, pk: int) -> Response:
        """
        Obtenção de usuário
        """
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def patch(self, request: Request, pk: int) -> Response:
        """
        Atualização de usuário
        """
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request: Request, pk: int) -> Response:
        """
        Deleção de usuário
        """
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
