# Linguanodon API

Backend providing source data for *linguanodon*.

## Development

See also:
  - [How to Add an Endpoint](/doc/adding-an-endpoint.md)

### Handling Languages

- Use BCP 47/[IETF language tag](https://en.wikipedia.org/wiki/IETF_language_tag) for language codes
- Language codes are stored directly in the models (e.g., 'en' for English, 'ar-EG' for Egyptian Arabic)

### Structure

- Define shared models in the `linguanodon` app and nowhere else
- Put logic directly related to those models in `linguanodon/interactors`
- Build endpoints in the `api` app
- Build custom, "function-based" endpoints without any framework
- Unit-test endpoints by adding tests in `api/tests`
  - For each test, add a `test_$function.py` file, as well as `test_$function_fixture.json` (for factory) and `test_$function_expected_response.json` (the HTTP response we want)
    - This way, we prevent unholy factory function hacks that nobody can read

### Testing

```bash
python manage.py test
```