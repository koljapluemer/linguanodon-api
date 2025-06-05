from django.http import JsonResponse
from entities.interactors.list_units_of_meaning_for_learning_goal import ListUnitsOfMeaningForLearningGoal
from entities.models import LearningGoal, UnitOfMeaning

def list_units_of_meaning_for_learning_goal(request, learning_goal_id):
    try:
        # Get pagination parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # Debug: Check if learning goal exists
        try:
            learning_goal = LearningGoal.objects.get(id=learning_goal_id)
            # Debug: Check units of meaning directly
            units = UnitOfMeaning.objects.filter(learning_goals=learning_goal)
            print(f"Found {units.count()} units of meaning for learning goal {learning_goal_id}")
            for unit in units:
                print(f"Unit {unit.id}: {unit.text}")
        except LearningGoal.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'Learning goal with id {learning_goal_id} not found'
            }, status=404)
        
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
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
