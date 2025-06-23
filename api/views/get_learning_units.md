# Internal API Documentation: /api/learning-goals/

This endpoint returns a paginated list of all learning goals (LearningUnit objects) with their `id`, `name`, `language_code`, and `updated_by_server_at`.

## How to use
- **URL:** `/api/learning-goals/`
- **Method:** GET
- **Pagination:**
  - Use the `page` query parameter to select the page (default: 1)
  - Example: `/api/learning-goals/?page=2`
- **Date filter:**
  - Use the `date` query parameter to only return learning goals updated on or after this date.
  - Format: `YYYY-MM-DD`
  - Example: `/api/learning-goals/?date=2024-06-01`

## Response shape
```
{
  "results": [
    {"id": 1, "name": "Goal 1", "language_code": "en", "updated_by_server_at": "2024-06-01T12:34:56.789Z"},
    {"id": 2, "name": "Goal 2", "language_code": "arz", "updated_by_server_at": "2024-06-02T09:00:00.000Z"},
    ... up to 50 per page ...
  ],
  "page": 1,
  "num_pages": 5
}
```
- `results`: List of learning goals for the current page
- `page`: Current page number
- `num_pages`: Total number of pages
- `updated_by_server_at`: ISO 8601 timestamp when the learning goal was last updated
