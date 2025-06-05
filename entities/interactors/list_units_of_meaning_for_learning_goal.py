from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from entities.models import LearningGoal, UnitOfMeaning

class ListUnitsOfMeaningForLearningGoal:
    def __init__(self, learning_goal_id: int, page: int = 1, page_size: int = 10):
        self.learning_goal_id = learning_goal_id
        self.page = page
        self.page_size = page_size

    def execute(self):
        # Get learning goal or 404
        learning_goal = get_object_or_404(LearningGoal, id=self.learning_goal_id)
        
        # Get units of meaning for the learning goal, ordered by ID
        units_of_meaning = UnitOfMeaning.objects.filter(
            learning_goals=learning_goal
        ).order_by('id')
        
        # Paginate results
        paginator = Paginator(units_of_meaning, self.page_size)
        page_obj = paginator.get_page(self.page)
        
        # Prepare response data
        data = [{'id': unit.id} for unit in page_obj]
        
        # Prepare pagination info
        pagination = {
            'total_items': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': self.page,
            'page_size': self.page_size,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous()
        }
        
        return {
            'status': 'success',
            'data': data,
            'pagination': pagination
        }
