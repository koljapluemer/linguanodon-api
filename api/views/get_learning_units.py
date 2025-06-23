from django.http import JsonResponse
from linguanodon.models.learning_unit import LearningUnit
import math

def get_learning_goals(request):
    # Pagination parameters
    page_size = 50
    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    # Query all learning units, now including language_code
    units = LearningUnit.objects.all().values('id', 'name', 'language_code')
    total = units.count()
    num_pages = math.ceil(total / page_size)
    start = (page - 1) * page_size
    end = start + page_size
    results = list(units[start:end])

    return JsonResponse({
        'results': results,
        'page': page,
        'num_pages': num_pages,
    })
