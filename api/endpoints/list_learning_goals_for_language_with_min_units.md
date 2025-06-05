# List Learning Goals for Language with Minimum Units

Lists all learning goals for a specific language that have at least a specified number of total items (units of meaning + child learning goals).

## Endpoint

```
GET /api/list_learning_goals_for_language_with_min_units/{language_code}/
```

## Parameters

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| language_code | string | The BCP 47 language code to get learning goals for (e.g., 'en' for English) |

### Query Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| page | integer | Page number (1-based) | 1 |
| page_size | integer | Number of items per page | 10 |
| min_units | integer | Minimum number of total items (units + children) | 1 |

## Response

### Success (200)

```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "name": "Basic Greetings",
            "unit_count": 3,
            "child_count": 2,
            "total_count": 5
        },
        {
            "id": 2,
            "name": "Numbers 1-10",
            "unit_count": 2,
            "child_count": 1,
            "total_count": 3
        }
    ],
    "pagination": {
        "total_items": 2,
        "total_pages": 1,
        "current_page": 1,
        "page_size": 10,
        "has_next": false,
        "has_previous": false
    }
}
```

### Error Responses

#### Invalid Parameters (400)

```json
{
    "status": "error",
    "message": "Invalid parameters"
}
```

#### Server Error (500)

```json
{
    "status": "error",
    "message": "Internal server error"
}
```

## Examples

### Basic Request

```bash
curl /api/list_learning_goals_for_language_with_min_units/en/?min_units=5
```

### With Pagination

```bash
curl /api/list_learning_goals_for_language_with_min_units/en/?page=2&page_size=20&min_units=3
``` 