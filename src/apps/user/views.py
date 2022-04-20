from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from django.contrib.auth.models import User

from .serializers import UserSerializer
from .filters import UserFilter

from rest_framework.permissions import IsAuthenticated


class UserListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    filterset_fields = ('username', 'email',)
    search_fields = ('username', 'email',)

    queryset = User.objects.order_by('username')

    serializer_class = UserSerializer
    filterset_class = UserFilter


class UserDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer
