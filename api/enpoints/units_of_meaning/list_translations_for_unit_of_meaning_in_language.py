from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from entities.models.unit_of_meaning import UnitOfMeaning
from entities.models.language import Language
from drf_spectacular.utils import extend_schema, OpenApiParameter

class UnitOfMeaningTranslationSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source='language.code')

    class Meta:
        model = UnitOfMeaning
        fields = ['id', 'text', 'language']

class UnitOfMeaningTranslationViewSet(viewsets.ViewSet):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='language_code',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Language code to get translations in (e.g., "es" for Spanish)',
                required=True
            )
        ],
        responses={200: None}
    )
    @action(detail=True, methods=['get'])
    def translations(self, request, pk=None):
        try:
            unit_of_meaning = UnitOfMeaning.objects.get(pk=pk)
            language_code = request.query_params.get('language_code')
            
            if not language_code:
                return Response(
                    {'error': 'language_code parameter is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                target_language = Language.objects.get(code=language_code)
            except Language.DoesNotExist:
                return Response(
                    {'error': f'Language with code {language_code} does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get translations that are in the target language
            translations = unit_of_meaning.translations.filter(language=target_language)
            
            serializer = UnitOfMeaningTranslationSerializer(unit_of_meaning)
            translations_serializer = UnitOfMeaningTranslationSerializer(translations, many=True)
            
            return Response({
                'unit_of_meaning': serializer.data,
                'translations': translations_serializer.data
            })
            
        except UnitOfMeaning.DoesNotExist:
            return Response(
                {'error': 'Unit of meaning not found'},
                status=status.HTTP_404_NOT_FOUND
            )
