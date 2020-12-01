from papers.models import Paper

from rest_framework import serializers


class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ('id',
                  'title',
                  'description',
                  'published_at',
                  'source_name',
                  'author',
                  'url',)
    # title = serializers.CharField(max_length=200)
    # published_at = serializers.DateField()
