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

- Make sentence-related objects:
  - Create a `LearningGoal`:
    - `name`: `sentence_arz`
    - `description`: None
    - `parents`: None
    - `language_code`: "arz"
  - Create a `UnitOfMeaning`:
    -  `text`: `sentence_arz`
    -  `language_code`: "arz"

## Misc Features

- Limit of sentences that will be scraped can be set by a constant at the top of the file
