from django.db import models

class LearningGoal(models.Model):
    language_code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    parents = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="children")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', 'name']
        unique_together = ('language_code', 'name')
    def __str__(self):
        return self.name

    def get_all_units_of_meaning(self):
        from entities.models.unit_of_meaning import UnitOfMeaning
        all_goal_ids = set()
        to_visit = [self]
        while to_visit:
            current = to_visit.pop()
            if current.id not in all_goal_ids:
                all_goal_ids.add(current.id)
                to_visit.extend(list(current.children.all()))
        return UnitOfMeaning.objects.filter(learning_goals__id__in=all_goal_ids).distinct()

