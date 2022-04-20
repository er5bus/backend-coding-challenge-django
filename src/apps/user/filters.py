from django_filters import filterset

from django.contrib.auth.models import User


class UserFilter(filterset.FilterSet):
    class Meta:
        model = User
        fields = ('username', 'email')
