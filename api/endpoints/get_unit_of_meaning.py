from django.http import JsonResponse
from entities.interactors.get_unit_of_meaning import get_unit_of_meaning as get_unit_details

def get_unit_of_meaning(request, unit_of_meaning_id):
    # Get data from interactor
    data = get_unit_details(unit_of_meaning_id=unit_of_meaning_id)
    
    return JsonResponse({
        'status': 'success',
        'data': data
    }) 