from django.http import JsonResponse
from linguanodon.models.learning_unit import LearningUnit
import math
from datetime import datetime

def get_learning_goals(request):
    # Pagination parameters
    page_size = 50
    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    # Date filter (YYYY-MM-DD)
    date_str = request.GET.get('date')
    date_filter = None
    if date_str:
        try:
            date_filter = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date_filter = None

    # Query all learning units, possibly filtered by date
    units_qs = LearningUnit.objects.all()
    if date_filter:
        units_qs = units_qs.filter(updated_at__date__gte=date_filter)
    units = units_qs.values('id', 'name', 'language_code', 'updated_at')
    total = units.count()
    num_pages = math.ceil(total / page_size)
    start = (page - 1) * page_size
    end = start + page_size
    results = [
        {
            'id': u['id'],
            'name': u['name'],
            'language_code': u['language_code'],
            'updated_by_server_at': u['updated_at'].isoformat() if hasattr(u['updated_at'], 'isoformat') else str(u['updated_at'])
        }
        for u in units[start:end]
    ]

    return JsonResponse({
        'results': results,
        'page': page,
        'num_pages': num_pages,
    })
