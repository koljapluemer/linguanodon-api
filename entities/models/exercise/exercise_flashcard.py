from entities.models.exercise.exercise import Exercise


class ExerciseFlashcard(Exercise):
    def __str__(self):
        return self.extra_content_before_solve + " | " + self.extra_content_after_solve
