# Get Unit of Meaning

Returns all details of a unit of meaning by its ID.

## Endpoint

```
GET /api/get_unit_of_meaning/{unit_of_meaning_id}/
```

## Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| unit_of_meaning_id | integer | The ID of the unit of meaning to get |

## Response

### Success (200)

```json
{
    "status": "success",
    "data": {
        "id": 1,
        "text": "Hola",
        "language": {
            "id": 2,
            "name": "Spanish",
            "code": "es"
        },
        "creation_context": "Test",
        "license": null,
        "owner": null,
        "owner_link": null,
        "source": null,
        "source_link": null,
        "updated_at": "2024-01-01T00:00:00Z"
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

## Example Usage

```bash
# Get details of unit of meaning with ID 1
curl /api/get_unit_of_meaning/1/
``` 