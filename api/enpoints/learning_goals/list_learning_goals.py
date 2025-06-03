from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from api.enpoints.learning_goals.serializers import LearningGoalSerializer
from entities.models.learning_goal import LearningGoal

class LearningGoalFilter(filters.FilterSet):
    language_code = filters.CharFilter(method='filter_by_language_code')
    updated_after = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')

    def filter_by_language_code(self, queryset, name, value):
        return queryset.filter(language__code=value)

    class Meta:
        model = LearningGoal
        fields = ['language_code', 'updated_after']

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class LearningGoalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LearningGoal.objects.all()
    serializer_class = LearningGoalSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = LearningGoalFilter
