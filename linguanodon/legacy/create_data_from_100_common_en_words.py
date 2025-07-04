import json
from pathlib import Path
from django.core.management.base import BaseCommand
from linguanodon.models import LearningGoal, UnitOfMeaning

class Command(BaseCommand):
    help = 'Creates the 100 most common English words with their learning goals'

    def handle(self, *args, **options):
        # Create parent learning goal
        parent_goal, created = LearningGoal.objects.get_or_create(
            name="Know the 100 most common words in English in Egyptian Arabic",
            language_code='ar-EG',
            defaults={
                'description': 'Master the 100 most frequently used English words and their meanings in Egyptian Arabic. This foundational vocabulary will help you understand and communicate in basic English conversations.'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created parent learning goal'))

        # Read the JSON file
        json_path = Path(__file__).parent / '100_common_words.json'
        try:
            with open(json_path, 'r') as f:
                words = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Could not find {json_path}'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'Invalid JSON in {json_path}'))
            return

        # Create UnitOfMeaning and LearningGoal for each word
        created_count = 0
        for word in words:
            # Create UnitOfMeaning for English word
            unit, created = UnitOfMeaning.objects.get_or_create(
                text=word,
                language_code='en'
            )
            
            if created:
                # Create individual learning goal
                word_goal = LearningGoal.objects.create(
                    name=f'Know the meaning of "{word}" in Egyptian Arabic',
                    language_code='ar-EG'
                )
                word_goal.parents.add(parent_goal)
                unit.learning_goals.add(word_goal)
                
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} words with their learning goals')) 