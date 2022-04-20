from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from .serializers import NoteSerializer
from .models import Note
from .filters import NoteFilter

from apps.core.permissions import IsCurrentUserOwnerOrReadOnly


class NoteListAPIView(ListCreateAPIView):
    permission_classes = (IsCurrentUserOwnerOrReadOnly,)

    filterset_fields = ('title', 'body', 'tags')
    search_fields = ('title', 'body', 'tags')
    ordering_fields = ('title', 'body',)

    queryset = Note.objects.prefetch_related('tags')

    serializer_class = NoteSerializer
    filterset_class = NoteFilter

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return self.queryset.filter(author=self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsCurrentUserOwnerOrReadOnly,)

    queryset = Note.objects.prefetch_related('tags')
    serializer_class = NoteSerializer

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return self.queryset.filter(author=self.request.user)
        return self.queryset

    def perform_destroy(self, instance):
        for tag in instance.tags.all():
            if not tag.notes:
                tag.delete()
        super().perform_destroy(instance)
