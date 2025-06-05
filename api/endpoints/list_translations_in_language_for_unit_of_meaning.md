# List Translations in Language for Unit of Meaning

Lists all translations of a unit of meaning in a specific language.

## Endpoint

```
GET /api/list_translations_in_language_for_unit_of_meaning/{unit_of_meaning_id}/{language_code}/
```

## Parameters

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| unit_of_meaning_id | integer | The ID of the unit of meaning to get translations for |
| language_code | string | The BCP 47 language code to get translations in (e.g., 'en' for English) |

### Query Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| page | integer | Page number (1-based) | 1 |
| page_size | integer | Number of items per page | 10 |

## Response

### Success (200)

```json
{
    "status": "success",
    "data": [
        {
            "id": 3
        },
        {
            "id": 4
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
    "message": "Invalid pagination parameters"
}
```

#### Not Found (404)

```json
{
    "status": "error",
    "message": "Unit of meaning not found"
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
curl /api/list_translations_in_language_for_unit_of_meaning/1/en/
```

### With Pagination

```bash
curl /api/list_translations_in_language_for_unit_of_meaning/1/en/?page=2&page_size=20
```
