from django.contrib import admin
from .models import LearningUnit, TanglibleLearningUnit

@admin.register(LearningUnit)
class LearningUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'language_code', 'updated_at')
    list_filter = ('language_code',)
    search_fields = ('name', 'description')
    filter_horizontal = ('parents',)

@admin.register(TanglibleLearningUnit)
class TanglibleLearningUnitAdmin(admin.ModelAdmin):
    list_display = ('text', 'type_info', 'language_code', 'updated_at')
    list_filter = ('language_code', 'type_info')
    search_fields = ('text', 'pronunciation', 'notes')
    filter_horizontal = ('translations', 'synonyms', 'similar_but_not_synonyms', 'parents')
