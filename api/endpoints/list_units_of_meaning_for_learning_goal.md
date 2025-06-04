# List Units of Meaning for Learning Goal

This endpoint returns a paginated list of units of meaning associated with a specific learning goal.

## Endpoint

```
GET /api/list_units_of_meaning_for_learning_goal/{learning_goal_id}/
```

## Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| learning_goal_id | integer | The ID of the learning goal to get units of meaning for |

## Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number (1-based) |
| page_size | integer | 10 | Number of items per page (max 100) |

## Response

### Success (200)

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

#### Learning Goal Not Found (404)

```json
{
    "status": "error",
    "message": "Learning goal with id 1 not found"
}
```

#### Invalid Pagination Parameters (400)

```json
{
    "status": "error",
    "message": "Invalid pagination parameters"
}
```

## Example Usage

```bash
# Get first page of units of meaning for learning goal with ID 1
curl /api/list_units_of_meaning_for_learning_goal/1/

# Get second page with 20 items per page