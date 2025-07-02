# Linguanodon API

Backend providing source data for *linguanodon*, built in Django.

Currently a local-only app generating JSON files.

*Not in use*

## Development

### Handling Languages

- Use BCP 47/[IETF language tag](https://en.wikipedia.org/wiki/IETF_language_tag) for language codes
- Language codes are stored directly in the models (e.g., 'en' for English, 'ar-EG' for Egyptian Arabic)

### Scripts

- All in `linguanodon/management/commands`
- Documentation per Script:
  - [LM Data Generation](./linguanodon/management/commands/create_data_from_lisaanmasry_sentences.md)
  - [JSON File Output](./linguanodon/management/commands/make_json_learning_goals.md)