from django.urls import re_path

from . import views


urlpatterns = (
    re_path(r'^notes/$',
            views.NoteListAPIView.as_view(),
            name='note-list'),
    re_path(r'^notes/(?P<pk>\d+)/$',
            views.NoteDetailAPIView.as_view(),
            name='note-detail'),
)
