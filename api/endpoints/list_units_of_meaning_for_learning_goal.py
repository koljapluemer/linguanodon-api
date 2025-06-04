from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from entities.models import LearningGoal, UnitOfMeaning

def list_units_of_meaning_for_learning_goal(request, learning_goal_id):
    # Get learning goal or 404
    learning_goal = get_object_or_404(LearningGoal, id=learning_goal_id)
    
    # Get pagination parameters
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    # Get units of meaning for the learning goal, ordered by ID to match expected response
    units_of_meaning = UnitOfMeaning.objects.filter(learning_goals=learning_goal).order_by('id')
    
    # Paginate results
    paginator = Paginator(units_of_meaning, page_size)
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
