from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from entities.models import UnitOfMeaning, Language

def list_translations_in_language_for_unit_of_meaning(unit_of_meaning_id: int, language_code: str, page: int = 1, page_size: int = 10):
    """
    List all translations of a unit of meaning in a specific language.
    
    Args:
        unit_of_meaning_id: The ID of the unit of meaning to get translations for
        language_code: The code of the language to get translations in
        page: Page number (1-based)
        page_size: Number of items per page
        
    Returns:
        tuple: (data, pagination_info)
            - data: List of dictionaries containing translation IDs
            - pagination_info: Dictionary containing pagination details
    """
    # Get unit of meaning or 404
    unit_of_meaning = get_object_or_404(UnitOfMeaning, id=unit_of_meaning_id)
    
    # Get language or 404
    language = get_object_or_404(Language, code=language_code)
    
    # Get translations in the specified language
    translations = UnitOfMeaning.objects.filter(
        translations=unit_of_meaning,
        language=language
    ).order_by('id')
    
    # Paginate results
    paginator = Paginator(translations, page_size)
    page_obj = paginator.get_page(page)
    
    # Prepare response data
    data = [{'id': unit.id} for unit in page_obj]
    
    # Prepare pagination info
    pagination = {
        'total_items': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page,
        'page_size': page_size,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous()
    }
    
    return data, pagination
