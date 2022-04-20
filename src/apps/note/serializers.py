from rest_framework import serializers

from .models import Note, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagListField(serializers.StringRelatedField):
    child = serializers.CharField()

    def to_internal_value(self, data):
        tag, _ = Tag.objects.get_or_create(name=data)
        return tag.pk


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'body', 'tags')

    tags = TagListField(many=True)

    def update(self, instance, validated_data):
        """ Remove unused tags """
        for tag in instance.tags.all():
            if tag.name not in validated_data.get('tags', [])\
                    and not tag.notes:
                tag.delete()
        return validated_data
