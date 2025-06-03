from django.contrib import admin
from entities.models import Language, LearningGoal, UnitOfMeaning, Translation

admin.site.register(Language)
admin.site.register(LearningGoal)
admin.site.register(UnitOfMeaning)
admin.site.register(Translation)
