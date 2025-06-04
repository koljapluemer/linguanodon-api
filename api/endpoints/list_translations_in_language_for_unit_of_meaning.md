# List Translations in Language for Unit of Meaning

Lists all translations of a unit of meaning in a specific language.

## Endpoint

```
GET /api/list_translations_in_language_for_unit_of_meaning/{unit_of_meaning_id}/{language_code}/
```

## Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| unit_of_meaning_id | integer | The ID of the unit of meaning to get translations for |
| language_code | string | The code of the language to get translations in (e.g., 'en' for English) |

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

#### Unit of Meaning Not Found (404)

```json
{
    "status": "error",
    "message": "Unit of meaning with id 1 not found"
}
```

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
# Get first page of English translations for unit of meaning with ID 1
curl /api/list_translations_in_language_for_unit_of_meaning/1/en/

# Get second page with 20 items per page
curl /api/list_translations_in_language_for_unit_of_meaning/1/en/?page=2&page_size=20
```
