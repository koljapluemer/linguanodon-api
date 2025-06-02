import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from entities.models import Language, LearningGoal, Template

class Command(BaseCommand):
    help = 'Creates templates for the 100 most common English words'

    def handle(self, *args, **options):
        # Get or create Egyptian Arabic language
        arz_language, created = Language.objects.get_or_create(
            name="Egyptian Arabic",
            code="arz"
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Egyptian Arabic language instance'))

        # Get or create admin user for creator
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('No admin user found. Please create one first.'))
            return

        # Get or create learning goal
        learning_goal, created = LearningGoal.objects.get_or_create(
            name="Know the most common 100 English words in Egyptian Arabic",
            language=arz_language,
            defaults={
                'description': 'Learn the 100 most common English words',
                'creator': admin_user,
                'is_public': True,
                'is_approved': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created learning goal'))

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

        # Create templates for each word
        created_count = 0
        for word in words:
            template, created = Template.objects.get_or_create(
                language=arz_language,
                field_translation=word,
                defaults={
                    'creator': admin_user,
                    'is_public': True,
                    'is_approved': True
                }
            )
            
            if created:
                template.learning_goals.add(learning_goal)
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} templates')) 