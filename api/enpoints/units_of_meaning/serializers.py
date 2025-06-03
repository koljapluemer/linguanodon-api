from rest_framework import serializers
from entities.models.unit_of_meaning import UnitOfMeaning

class UnitOfMeaningSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnitOfMeaning
        fields = ['id']

