from django_filters import filterset, filters

from .models import Note


class NoteFilter(filterset.FilterSet):
    tag = filters.CharFilter(method='tags_filter')

    def tags_filter(self, queryset, name, value):
        return queryset.filter(tags__name__icontains=value)

    class Meta:
        model = Note
        fields = ('title', 'body', 'tag')
