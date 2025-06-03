from rest_framework import serializers
from entities.models.translation import Translation

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = [
            'id', 
            'text',
            'creation_context',
            'license',
            'owner',
            'owner_link',
            'source',
            'source_link'
        ]
