from django.urls import re_path

from . import views


urlpatterns = (
    re_path(r'^users/$',
            views.UserListAPIView.as_view(),
            name='user-list'),
    re_path(r'^users/(?P<pk>\d+)/$',
            views.UserDetailAPIView.as_view(),
            name='user-detail'),
)
