from typing import List, Tuple
from django.core.paginator import Paginator
from entities.models.learning_goal import LearningGoal

def list_learning_goals_for_language(language_code: str, page: int = 1, page_size: int = 10) -> Tuple[List[LearningGoal], dict]:
    """
    List all learning goals for a specific language with pagination.
    
    Args:
        language_code (str): The BCP 47 language code to get learning goals for
        page (int): The page number to return (1-based)
        page_size (int): Number of items per page
        
    Returns:
        Tuple[List[LearningGoal], dict]: A tuple containing:
            - List of learning goals for the specified language
            - Pagination metadata including total pages and items
    """
    queryset = LearningGoal.objects.filter(language_code=language_code).only('id', 'name').order_by('id')
    
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    
    pagination_meta = {
        'total_items': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page,
        'page_size': page_size,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
    }
    
    return list(page_obj), pagination_meta
