# List Units of Meaning for Learning Goal

This endpoint returns a paginated list of units of meaning associated with a specific learning goal.

## Endpoint

```
GET /api/learning-goals/{learning_goal_id}/units-of-meaning
```

## URL Parameters

- `learning_goal_id` (integer, required): The ID of the learning goal to get units of meaning for

## Query Parameters

- `page` (integer, optional): The page number to retrieve. Defaults to 1.
- `page_size` (integer, optional): Number of items per page. Defaults to 10.

## Response

### Success Response (200 OK)

```json
{
    "status": "success",
    "data": [
        {
            "id": 1
        },
        {
            "id": 2
        },
        {
            "id": 4
        }
    ],
    "pagination": {
        "total_items": 3,
        "total_pages": 1,
        "current_page": 1,
        "page_size": 10,
        "has_next": false,
        "has_previous": false
    }
}
```

### Error Responses

- `404 Not Found`: If the learning goal with the specified ID does not exist

## Example Usage

```bash
curl -X GET "http://localhost:8000/api/learning-goals/1/units-of-meaning?page=1&page_size=10"
```
