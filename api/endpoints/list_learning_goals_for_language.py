from django.http import JsonResponse
from django.views import View
from entities.interactors.list_learning_goals_for_language import list_learning_goals_for_language

class ListLearningGoalsForLanguageView(View):
    def get(self, request, language_code):
        try:
            # Get pagination parameters from query string
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            
            # Ensure page and page_size are positive
            page = max(1, page)
            page_size = max(1, min(page_size, 100))  # Cap at 100 items per page
            
            learning_goals, pagination_meta = list_learning_goals_for_language(
                language_code=language_code,
                page=page,
                page_size=page_size
            )
            
            # Convert learning goals to dictionary format with only id and name
            goals_data = [
                {
                    'id': goal.id,
                    'name': goal.name
                }
                for goal in learning_goals
            ]
            
            return JsonResponse({
                'status': 'success',
                'data': goals_data,
                'pagination': pagination_meta
            })
            
        except ValueError as e:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid pagination parameters'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
