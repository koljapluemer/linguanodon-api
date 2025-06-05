from django.shortcuts import get_object_or_404
from entities.models import UnitOfMeaning

def get_unit_of_meaning(unit_of_meaning_id: int):
    """
    Get all details of a unit of meaning by its ID.
    
    Args:
        unit_of_meaning_id: The ID of the unit of meaning to get
        
    Returns:
        dict: Dictionary containing all unit of meaning details
    """
    # Get unit of meaning or 404
    unit = get_object_or_404(UnitOfMeaning, id=unit_of_meaning_id)
    
    # Prepare response data
    return {
        'id': unit.id,
        'text': unit.text,
        'language_code': unit.language_code,
        'creation_context': unit.creation_context,
        'license': unit.license,
        'owner': unit.owner,
        'owner_link': unit.owner_link,
        'source': unit.source,
        'source_link': unit.source_link,
        'updated_at': unit.updated_at.strftime('%Y-%m-%dT%H:%M:%SZ')
    } 