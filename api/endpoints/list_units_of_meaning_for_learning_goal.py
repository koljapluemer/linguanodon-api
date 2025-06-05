from django.http import JsonResponse
from entities.interactors.list_units_of_meaning_for_learning_goal import ListUnitsOfMeaningForLearningGoal

def list_units_of_meaning_for_learning_goal(request, learning_goal_id):
    try:
        # Get pagination parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # Execute interactor
        interactor = ListUnitsOfMeaningForLearningGoal(
            learning_goal_id=learning_goal_id,
            page=page,
            page_size=page_size
        )
        result = interactor.execute()
        
        return JsonResponse(result)
        
    except ValueError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid pagination parameters'
        }, status=400)
