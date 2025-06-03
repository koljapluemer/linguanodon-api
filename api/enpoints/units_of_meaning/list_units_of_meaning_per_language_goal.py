from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from entities.models.unit_of_meaning import UnitOfMeaning
from api.enpoints.units_of_meaning.serializers import UnitOfMeaningSerializer
from django.utils import timezone

class UnitOfMeaningFilter(filters.FilterSet):
    learning_goal_id = filters.NumberFilter(field_name='learning_goals__id')
    updated_after = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')

    class Meta:
        model = UnitOfMeaning
        fields = ['learning_goal_id', 'updated_after']

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UnitOfMeaningViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UnitOfMeaning.objects.all()
    serializer_class = UnitOfMeaningSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = UnitOfMeaningFilter
