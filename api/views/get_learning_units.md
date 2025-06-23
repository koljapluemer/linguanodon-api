# Internal API Documentation: /api/learning-goals/

This endpoint returns a paginated list of all learning goals (LearningUnit objects) with their `id` and `name`.

## How to use
- **URL:** `/api/learning-goals/`
- **Method:** GET
- **Pagination:**
  - Use the `page` query parameter to select the page (default: 1)
  - Example: `/api/learning-goals/?page=2`

## Response shape
```
{
  "results": [
    {"id": 1, "name": "Goal 1"},
    {"id": 2, "name": "Goal 2"},
    ... up to 50 per page ...
  ],
  "page": 1,
  "num_pages": 5
}
```
- `results`: List of learning goals for the current page
- `page`: Current page number
- `num_pages`: Total number of pages
