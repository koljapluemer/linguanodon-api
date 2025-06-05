# Make JSON Learning Goals

This script generates JSON files for learning units that have sufficient relationships (children or parents) to be considered meaningful learning goals. It creates a structured output that can be used by frontend applications to display learning content.

## Configuration

The script uses several configuration constants:
- `MIN_CHILDREN_COUNT`: Minimum number of children a learning unit must have to be included (default: 3)
- `MIN_PARENTS_COUNT`: Minimum number of parents a learning unit must have to be included (default: 3)
- `TARGET_LANGUAGE_CODE`: Language code to filter learning units by (default: 'arz')

## Output Structure

The script generates three types of files in the `learning_units_json` directory:

1. `index.json`: Contains metadata about all valid learning units
2. `learning_unit_{id}.json`: Contains basic information about a specific learning unit
3. `learning_unit_{id}_tangible_units.json`: Contains all related tangible learning units
4. `types.ts`: TypeScript type definitions for the JSON structure

## Data Collection Process

### 1. Finding Valid Learning Units
- Filters learning units by target language code
- Includes units that have either:
  - At least MIN_CHILDREN_COUNT children
  - At least MIN_PARENTS_COUNT parents

### 2. Collecting Related Tangible Units
For each valid learning unit, the script collects:
- The unit itself (if it's a TanglibleLearningUnit)
- All children that are TanglibleLearningUnits
- All parents that are TanglibleLearningUnits (if the unit has sufficient parents)
- All translations of the above units

### 3. Relationship Handling
The script maintains several types of relationships:
- Parent-child relationships
- Translations between units
- Synonyms between units
- Similar but not synonym relationships

## Helper Functions

### get_all_related_translations(units)
- Takes a set of TanglibleLearningUnits
- Recursively collects all translations of these units
- Returns a distinct set of all related units

### get_recursive_children(unit)
- Takes a LearningUnit
- Recursively collects all children
- Returns a set of all child units

### get_all_related_tangible_units(unit)
- Takes a LearningUnit
- Collects all related TanglibleLearningUnits including:
  - The unit itself (if tangible)
  - All tangible children
  - All tangible parents (if unit has sufficient parents)
  - All translations of the above
- Returns a distinct set of all related tangible units

### clean_dict(d)
- Removes empty values from dictionaries
- Used to clean up JSON output

## TypeScript Types

The script generates TypeScript types for:
- LearningUnit
- TanglibleLearningUnit
- LearningUnitIndex
- File types for each JSON file
- Helper types for loading files

## Usage

Run the script using Django's management command:
```bash
python manage.py make_json_learning_goals
```

## Output Example

```json
// index.json
[
  {
    "id": 63,
    "name": "Learn \"أنا َ بـَجو َع طول ا ِلو َقت\"",
    "children_count": 8,
    "parents_count": 0
  }
]

// learning_unit_63.json
{
  "id": 63,
  "name": "Learn \"أنا َ بـَجو َع طول ا ِلو َقت\"",
  "language_code": "arz",
  "creation_context": "Lisaan Masry Script"
}

// learning_unit_63_tangible_units.json
[
  {
    "id": 65,
    "text": "أنا",
    "language_code": "arz",
    "type_info": "pronoun",
    "translations": [66],
    "parents": [63]
  }
]
```

## Notes

- The script uses Django's model inheritance to properly identify TanglibleLearningUnits
- All relationships are preserved in the output
- Empty values are removed from the JSON output for cleaner data
- The script includes debug logging to track the collection process
