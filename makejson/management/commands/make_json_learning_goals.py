import json
import os
from django.core.management.base import BaseCommand
from entities.models import LearningUnit, TanglibleLearningUnit

# Configuration constants
MIN_CHILDREN_COUNT = 3  # Minimum number of children for a learning unit to be included
MIN_PARENTS_COUNT = 3   # Minimum number of parents for a learning unit to be included
TARGET_LANGUAGE_CODE = 'arz'  # Language code to filter by

def get_all_related_translations(units):
    """Get all units of meaning and their translations for a given set of units"""
    # Start with the given units
    all_unit_ids = {unit.id for unit in units}
    to_process = all_unit_ids.copy()
    processed = set()

    # Recursively get all translations
    while to_process:
        current_id = to_process.pop()
        if current_id in processed:
            continue
        processed.add(current_id)
        
        # Get translations of current unit
        current_unit = TanglibleLearningUnit.objects.get(id=current_id)
        current_translations = current_unit.translations.values_list('id', flat=True)
        print(f"Unit {current_id} has {len(current_translations)} translations")
        all_unit_ids.update(current_translations)
        to_process.update(current_translations)

    # Return all units including translations
    return TanglibleLearningUnit.objects.filter(id__in=all_unit_ids).distinct()

def get_recursive_children(unit):
    """Get all children and their children recursively"""
    all_children = set()
    to_process = {unit}
    processed = set()

    while to_process:
        current = to_process.pop()
        if current.id in processed:
            continue
        processed.add(current.id)
        
        # Get direct children
        children = current.children.all()
        all_children.update(children)
        to_process.update(children)

    return all_children

def get_all_related_tangible_units(unit):
    """Get all TanglibleLearningUnits related to a LearningUnit through children or translations"""
    # First get all children recursively
    all_children = get_recursive_children(unit)
    print(f"Found {len(all_children)} total children for unit {unit.id}")
    
    # Get all TanglibleLearningUnits that are children
    tangible_units = set()
    
    # First check if the unit itself is a TanglibleLearningUnit
    try:
        tangible_unit = unit.tangliblelearningunit
        tangible_units.add(tangible_unit)
        print(f"Added parent tangible unit {tangible_unit.id} ({tangible_unit.text})")
    except TanglibleLearningUnit.DoesNotExist:
        print(f"Parent unit {unit.id} is not a tangible unit")
    
    # Then process children
    for child in all_children:
        try:
            tangible_unit = child.tangliblelearningunit
            tangible_units.add(tangible_unit)
            print(f"Added child tangible unit {tangible_unit.id} ({tangible_unit.text})")
        except TanglibleLearningUnit.DoesNotExist:
            print(f"Skipping non-tangible unit {child.id} ({child.name})")
    
    # If this unit has many parents, include tangible parents and their translations
    if unit.parents.count() >= MIN_PARENTS_COUNT:
        print(f"Unit {unit.id} has {unit.parents.count()} parents, checking for tangible parents")
        for parent in unit.parents.all():
            try:
                tangible_parent = parent.tangliblelearningunit
                tangible_units.add(tangible_parent)
                print(f"Added parent's tangible unit {tangible_parent.id} ({tangible_parent.text})")
            except TanglibleLearningUnit.DoesNotExist:
                print(f"Skipping non-tangible parent {parent.id} ({parent.name})")
    
    print(f"Found {len(tangible_units)} tangible units in children and parents")
    
    # Now get all translations of these tangible units
    all_related = get_all_related_translations(tangible_units)
    print(f"Found {len(all_related)} total related units including translations")
    
    return all_related

def clean_dict(d):
    """Remove empty values from a dictionary"""
    return {k: v for k, v in d.items() if v not in (None, "", [], {})}

class Command(BaseCommand):
    help = 'Creates JSON files for learning units with sufficient children or parents'

    def handle(self, *args, **options):
        # Create output directory if it doesn't exist
        output_dir = 'learning_units_json'
        os.makedirs(output_dir, exist_ok=True)

        # Get learning units with sufficient children or parents
        learning_units = LearningUnit.objects.filter(language_code=TARGET_LANGUAGE_CODE)
        valid_units = []
        index_data = []

        for unit in learning_units:
            children_count = unit.children.count()
            parents_count = unit.parents.count()
            
            if children_count >= MIN_CHILDREN_COUNT or parents_count >= MIN_PARENTS_COUNT:
                valid_units.append(unit)
                index_data.append({
                    'id': unit.id,
                    'name': unit.name,
                    'children_count': children_count,
                    'parents_count': parents_count
                })
                print(f"Found valid unit {unit.id} with {children_count} children and {parents_count} parents")

        # Create index file
        with open(os.path.join(output_dir, 'index.json'), 'w') as f:
            json.dump(index_data, f, indent=2)

        # Process each valid learning unit
        for unit in valid_units:
            print(f"\nProcessing unit {unit.id} ({unit.name})")
            
            # 1. Create learning unit file with basic info
            unit_data = clean_dict({
                'id': unit.id,
                'name': unit.name,
                'description': unit.description,
                'updated_at': unit.updated_at.isoformat(),
                'language_code': unit.language_code,
                'creation_context': unit.creation_context
            })
            with open(os.path.join(output_dir, f'learning_unit_{unit.id}.json'), 'w') as f:
                json.dump(unit_data, f, indent=2)

            # 2. Create related tangible units file
            all_related = get_all_related_tangible_units(unit)
            print(f"Found {len(all_related)} related tangible units for unit {unit.id}")
            
            tangible_units_data = []
            for tangible_unit in all_related:
                unit_data = clean_dict({
                    'id': tangible_unit.id,
                    'text': tangible_unit.text,
                    'language_code': tangible_unit.language_code,
                    'pronunciation': tangible_unit.pronunciation,
                    'type_info': tangible_unit.type_info,
                    'notes': tangible_unit.notes,
                    'creation_context': tangible_unit.creation_context,
                    'license': tangible_unit.license,
                    'owner': tangible_unit.owner,
                    'owner_link': tangible_unit.owner_link,
                    'source': tangible_unit.source,
                    'source_link': tangible_unit.source_link,
                    'translations': list(tangible_unit.translations.values_list('id', flat=True)),
                    'synonyms': list(tangible_unit.synonyms.values_list('id', flat=True)),
                    'similar_but_not_synonyms': list(tangible_unit.similar_but_not_synonyms.values_list('id', flat=True)),
                    'parents': list(tangible_unit.parents.values_list('id', flat=True))
                })
                tangible_units_data.append(unit_data)
            with open(os.path.join(output_dir, f'learning_unit_{unit.id}_tangible_units.json'), 'w') as f:
                json.dump(tangible_units_data, f, indent=2)

        # Create TypeScript types file
        types_content = """// Generated types for learning units data

// Base types for individual entities
export interface LearningUnit {
    id: number;
    name: string;
    description?: string;
    updated_at: string;
    language_code: string;
    creation_context?: string;
}

export interface TanglibleLearningUnit {
    id: number;
    text: string;
    language_code: string;
    pronunciation?: string;
    type_info?: string;
    notes?: string;
    creation_context?: string;
    license?: string;
    owner?: string;
    owner_link?: string;
    source?: string;
    source_link?: string;
    translations?: number[];
    synonyms?: number[];
    similar_but_not_synonyms?: number[];
    parents?: number[];
}

export interface LearningUnitIndex {
    id: number;
    name: string;
    children_count: number;
    parents_count: number;
}

// File types for each JSON file
export type LearningUnitFile = LearningUnit;
export type LearningUnitTangibleUnitsFile = TanglibleLearningUnit[];
export type LearningUnitIndexFile = LearningUnitIndex[];

// Helper type for loading files
export type LearningUnitFiles = {
    main: LearningUnitFile;
    tangible_units: LearningUnitTangibleUnitsFile;
}

// Example usage:
// const files: LearningUnitFiles = {
//     main: await import('./learning_unit_39.json'),
//     tangible_units: await import('./learning_unit_39_tangible_units.json')
// };
"""
        with open(os.path.join(output_dir, 'types.ts'), 'w') as f:
            f.write(types_content)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created JSON files for {len(valid_units)} learning units')
        )
