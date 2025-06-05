from django.http import JsonResponse
from django.views import View
from django.db.models import Count, Q, F
from entities.models.learning_goal import LearningGoal

class ListLearningGoalsForLanguageWithMinUnitsView(View):
    def get(self, request, language_code):
        try:
            # Get pagination parameters from query string
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            min_units = int(request.GET.get('min_units', 1))
            
            # Ensure parameters are positive
            page = max(1, page)
            page_size = max(1, min(page_size, 100))  # Cap at 100 items per page
            min_units = max(0, min_units)  # Ensure min_units is non-negative
            
            # Query learning goals with minimum units of meaning and child learning goals
            learning_goals = LearningGoal.objects.filter(
                language_code=language_code
            ).annotate(
                unit_count=Count('unitofmeaning'),
                child_count=Count('children')
            ).annotate(
                total_count=F('unit_count') + F('child_count')
            ).filter(
                total_count__gte=min_units
            )
            
            # Calculate pagination
            total_items = learning_goals.count()
            total_pages = (total_items + page_size - 1) // page_size
            
            # Apply pagination
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            learning_goals = learning_goals[start_idx:end_idx]
            
            # Convert learning goals to dictionary format
            goals_data = [
                {
                    'id': goal.id,
                    'name': goal.name,
                    'unit_count': goal.unit_count,
                    'child_count': goal.child_count,
                    'total_count': goal.total_count
                }
                for goal in learning_goals
            ]
            
            pagination_meta = {
                'total_items': total_items,
                'total_pages': total_pages,
                'current_page': page,
                'page_size': page_size,
                'has_next': page < total_pages,
                'has_previous': page > 1
            }
            
            return JsonResponse({
                'status': 'success',
                'data': goals_data,
                'pagination': pagination_meta
            })
            
        except ValueError as e:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid parameters'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500) 