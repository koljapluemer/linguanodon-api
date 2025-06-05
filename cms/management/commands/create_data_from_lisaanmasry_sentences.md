# Create Data From Lisaan Masry Example Sentences

- Intent: Use the excellent lm example sentences as a source for learning data (including the individual words that make up the sentences)

## Process

1. Go to [this link](https://eu.lisaanmasry.org/online/example.php)
2. Then, scrape:

- Find the Arabic sentence: 
  - Within `#example`, get first `p.ar`. Save the raw text content as `sentence_arz`

- Find the transliteration:
  - Within `#example`, find the first `<p>` which contains the string "Individual words:". Then, save the raw text content minus the string "Individual words:" (and trimmed) as `sentence_transliteration`

- Find the English translation:
  - Find the `<p>` element that follows the `<h3>` containing "Translation" directly as a sibling
  - Save the raw text content of that `<p>` as `sentence_en` 

- Find sentence notes
  - they may or may not exist (no problem if not)
  - if they exist, they must be within!! `#example`
  - they consistent of a `<p>` that directly follows a `<h3>` with the content "Notes" — as a sibling
  - Save notes or empty string as `sentence_notes`

- Make sentence-related objects:
  - Create a `LearningGoal`:
    - `name`: `sentence_arz`
    - `description`: None
    - `parents`: None
    - `language_code`: "arz"
  - Create a `UnitOfMeaning` for the arz sentence:
    -  `text`: `sentence_arz`
    -  `language_code`: "arz"
    -  `pronunciation`: `sentence_transliteration`
    -  `type_info`: Null
    -  `notes`: `sentence_notes`
    -  `translations`, `synonyms`, `similar_but_not_synonyms`: [] for now
    -  `learning_goals`: add the learning goal created above
    -  `creation_context`: "Lisaan Masry Script"
    -  `license`: "Copyright © 2007-2020 Mike Green — non-commercial use"
    -  `owner`: "Lisaan Masry"
    -  `owner_link`: "https://eu.lisaanmasry.org/info/en/copyright.html"
    -  `source`: "Lisaan Masry Examples"
    -  `source_link`: "https://eu.lisaanmasry.org/online/example.php"
  - Create a `UnitOfMeaning` for the en sentence:
    -  `text`: `sentence_en`
    -  `language_code`: "en"
    -  `pronunciation`: Null
    -  `type_info`: Null
    -  `notes`: Null
    -  `translations`: add the UnitOfMeaning of the arz sentence 
    -  `synonyms`, `similar_but_not_synonyms`: [] 
    -  `learning_goals`: add the learning goal created above
    -  `creation_context`: "Lisaan Masry Script"
    -  `license`: "Copyright © 2007-2020 Mike Green — non-commercial use"
    -  `owner`: "Lisaan Masry"
    -  `owner_link`: "https://eu.lisaanmasry.org/info/en/copyright.html"
    -  `source`: "Lisaan Masry Examples"
    -  `source_link`: "https://eu.lisaanmasry.org/online/example.php"

## Misc Features

- Limit of sentences that will be scraped can be set by a constant at the top of the file
