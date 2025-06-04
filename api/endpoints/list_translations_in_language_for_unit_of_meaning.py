from django.http import JsonResponse
from entities.interactors.list_translations_in_language_for_unit_of_meaning import list_translations_in_language_for_unit_of_meaning as get_translations

def list_translations_in_language_for_unit_of_meaning(request, unit_of_meaning_id, language_code):
    # Get pagination parameters
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    # Get data from interactor
    data, pagination = get_translations(
        unit_of_meaning_id=unit_of_meaning_id,
        language_code=language_code,
        page=page,
        page_size=page_size
    )
    
    return JsonResponse({
        'status': 'success',
        'data': data,
        'pagination': pagination
    }) 