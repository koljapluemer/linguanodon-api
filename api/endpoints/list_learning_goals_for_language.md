# List Learning Goals for Language

Lists all learning goals for a specific language.

## Endpoint

```
GET /list_learning_goals_for_language/{language_code}/
```

## Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| language_code | string | The code of the language to get learning goals for (e.g., 'en' for English) |

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
            "id": 1,
            "name": "Basic Greetings"
        },
        {
            "id": 2,
            "name": "Numbers 1-10"
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

#### Language Not Found (404)

```json
{
    "status": "error",
    "message": "Language with code en not found"
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
# Get first page of English learning goals
curl http://localhost:8081/list_learning_goals_for_language/en/

# Get second page with 20 items per page
curl http://localhost:8081/list_learning_goals_for_language/en/?page=2&page_size=20
``` 