import json
import os
from django.core.management.base import BaseCommand
from entities.models import LearningGoal, UnitOfMeaning

def get_all_related_translations(units):
    """Get all units of meaning and their translations for a given set of units"""
    # Start with the given units
    all_unit_ids = set(units.values_list('id', flat=True))
    to_process = all_unit_ids.copy()
    processed = set()

    # Recursively get all translations
    while to_process:
        current_id = to_process.pop()
        if current_id in processed:
            continue
        processed.add(current_id)
        
        # Get translations of current unit
        current_translations = UnitOfMeaning.objects.filter(
            id=current_id
        ).values_list('translations', flat=True)
        all_unit_ids.update(current_translations)
        to_process.update(current_translations)

    # Return all units including translations
    return UnitOfMeaning.objects.filter(id__in=all_unit_ids).distinct()

class Command(BaseCommand):
    help = 'Creates JSON files for learning goals with at least 3 units of meaning'

    def handle(self, *args, **options):
        # Create output directory if it doesn't exist
        output_dir = 'learning_goals_json'
        os.makedirs(output_dir, exist_ok=True)

        # Get learning goals with at least 3 units of meaning
        learning_goals = LearningGoal.objects.all()
        valid_goals = []
        index_data = []

        for goal in learning_goals:
            units = goal.get_all_related_units()
            if units.count() >= 3:
                valid_goals.append(goal)
                index_data.append({
                    'id': goal.id,
                    'name': goal.name
                })

        # Create index file
        with open(os.path.join(output_dir, 'index.json'), 'w') as f:
            json.dump(index_data, f, indent=2)

        # Process each valid learning goal
        for goal in valid_goals:
            # 1. Create learning goal file with basic info and ID lists
            goal_data = {
                'id': goal.id,
                'name': goal.name,
                'description': goal.description,
                'updated_at': goal.updated_at.isoformat(),
                'recursive_child_learning_goals': [g.id for g in goal.get_recursive_child_goals()],
                'directly_related_units_of_meaning': [u.id for u in goal.get_directly_related_units()]
            }
            with open(os.path.join(output_dir, f'learning_goal_{goal.id}.json'), 'w') as f:
                json.dump(goal_data, f, indent=2)

            # 2. Create child learning goals file
            child_goals_data = [
                {
                    'id': g.id,
                    'name': g.name,
                    'description': g.description
                }
                for g in goal.get_recursive_child_goals()
            ]
            with open(os.path.join(output_dir, f'learning_goal_{goal.id}_children.json'), 'w') as f:
                json.dump(child_goals_data, f, indent=2)

            # 3. Create units of meaning file
            # First get all units related to this goal and its children
            base_units = goal.get_all_related_units()
            # Then get all translations of these units
            all_units = get_all_related_translations(base_units)
            
            units_data = []
            for unit in all_units:
                unit_data = {
                    'id': unit.id,
                    'text': unit.text,
                    'language_code': unit.language_code,
                    'pronunciation': unit.pronunciation,
                    'type_info': unit.type_info,
                    'notes': unit.notes,
                    'creation_context': unit.creation_context,
                    'license': unit.license,
                    'owner': unit.owner,
                    'owner_link': unit.owner_link,
                    'source': unit.source,
                    'source_link': unit.source_link,
                    'translations': list(unit.translations.values_list('id', flat=True)),
                    'synonyms': list(unit.synonyms.values_list('id', flat=True)),
                    'similar_but_not_synonyms': list(unit.similar_but_not_synonyms.values_list('id', flat=True)),
                    'learning_goals': list(unit.learning_goals.values_list('id', flat=True))
                }
                units_data.append(unit_data)
            with open(os.path.join(output_dir, f'learning_goal_{goal.id}_units.json'), 'w') as f:
                json.dump(units_data, f, indent=2)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created JSON files for {len(valid_goals)} learning goals')
        )
