from django.db import models
from entities.models.unit_of_meaning import UnitOfMeaning

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

    def get_recursive_child_goals(self):
        """Get all child learning goals recursively"""
        child_goals = set()
        to_visit = list(self.children.all())
        while to_visit:
            current = to_visit.pop()
            if current.id not in child_goals:
                child_goals.add(current)
                to_visit.extend(list(current.children.all()))
        return child_goals

    def get_directly_related_units(self):
        """Get units directly related to this learning goal"""
        return UnitOfMeaning.objects.filter(learning_goals=self)

    def get_all_related_units(self):
        """Get all units of meaning related to this learning goal and its children"""
        all_goal_ids = {self.id} | {g.id for g in self.get_recursive_child_goals()}
        return UnitOfMeaning.objects.filter(learning_goals__id__in=all_goal_ids).distinct()

