from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from entities.models import UnitOfMeaning, Language

def list_translations_in_language_for_unit_of_meaning(request, unit_of_meaning_id, language_code):
    # Get unit of meaning or 404
    unit_of_meaning = get_object_or_404(UnitOfMeaning, id=unit_of_meaning_id)
    
    # Get language or 404
    language = get_object_or_404(Language, code=language_code)
    
    # Get pagination parameters
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
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
    
    return JsonResponse({
        'status': 'success',
        'data': data,
        'pagination': pagination
    }) 