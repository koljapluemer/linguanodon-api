from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from entities.models.translation import Translation
from api.enpoints.translations.serializers import TranslationSerializer
from django.utils import timezone

class TranslationFilter(filters.FilterSet):
    unit_of_meaning_id = filters.NumberFilter(field_name='unit_of_meaning__id')
    language_code = filters.CharFilter(field_name='language__code')
    updated_after = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')

    class Meta:
        model = Translation
        fields = ['unit_of_meaning_id', 'language_code', 'updated_after']

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TranslationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = TranslationFilter
