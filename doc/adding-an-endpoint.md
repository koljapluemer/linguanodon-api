# How to add an API Endpoint

## Good to Know

- Since we use a couple highly idiosyncratic endpoints, we follow no per-class API structure (neither in the code nor in the url naming)
- We use no framework or library for REST 

## Process

1. Add a failing Test
   - ...in `api/tests`
   - add 3 files:
     - `test_$functionname.py`: The test (loading the fixture and checking against expectation)
     - `test_$functionname_fixture.json`: Django objects represented as JSON
     - `test_$functionname_expected_response.json`: The object the API call should return
   - Tip: works fairly well to copy-paste an existing `response.json`, adapting it to cover the format you want, then let AI autofill the rest
2. Ensure the test is red, but not for stupid reasons
3. Green the test by adding the following:
   - An interactor script in `entities/interactors/$functionname.py`, handling direct interaction with Django ORM
   - The endpoint script itself, in `api/endpoints/`
   - A `.md` file in `api/endpoints/` with the same name, documenting the endpoint
4. Ensure test is green. 