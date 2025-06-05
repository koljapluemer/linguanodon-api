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
    -  `source`: "Lisaan Masry Example # `sentence_number`"
    -  `source_link`: "https://eu.lisaanmasry.org/online/example.php"


- Then, create word-based objects. First, based on the Arabic:

  - Find the `<p.ar>` within `#example` again (or save it, earlier). Find all `<span>` tags within. Click them one by one, and execute the following for each.
  
    - Note: Each of the following mentioned elements may not exist. In that case, skip the word and go to the next word.
    - Note: Clicking a word changes stuff on the page. You need to get all the following elements again for the following steps to work.
    - Find the sentence number:
      - find a `<td>` with text content of the *form* (exact numbers may change) "example 770 of 1532". Save the first number as `sentence_number`
    - Find the word's element type:
      - Find the first `tr` within `#word` that contains the string "Element:"
      - In that `<tr>`, find the *second* `<td>`, and save that as `word_base_type`
    - Find the word's language:
      - Find the first `tr` within `#word` that contains the string "Language:"
        - In that `<tr>`, find the *second* `<td>`
        - It's content may either be "MS" or "EG"
        - If it's "MS", set `word_lang` to "arb", if it's "EG", set `word_lang` to "arz"
  
    - Find the all the word's forms
      - This will be an array of objects
      - Find the first `<table>` following as direct sibling behind an `<h1>` with the content "Forms"
      - Loop this table's `<tr>`. For each:
        - Get the second `<td>` within in the row
          - In that, look for a `<b>` tag. It's content should be saved (within the loop iteration) as `form_transliteration`
          - In the same `<td`> look for an `<i>` tag. If it does not exist, do not worry, it's not critical. If it exist, save content as `form_type`
        - Get the third `td` of the row
          - Save its content as `form_arabic`
        - If it's the first `<tr>` of this table (ONLY THEN!!), make a `LearningGoal`:
          - `language_code`: "arz"
          - `name`: `form_arabic`
          - no `description`
          - `parents`: add the sentence's language goal created earlier
        - Then, for *every* `<tr>` of the table, create a `UnitOfMeaning`. Save references, we're going to need them later:
          - `text`: `form_arabic`
          - `language_code`: `word_lang`
          - `pronunciation`: `form_transliteration`
          - `type_info`: `word_base_type` + " " + `form_type`
          - `notes`: Null
          - `translations:` None, for now
          - `synonyms`: []
          - `similar_but_not_synonyms`: Add references to all other objects that were created looping this table. If a table as 4 `<tr>`, each created `UnitOfMeaning` should in this field link to the other 3
          - `learning_goals`: add the language goal created in the step above
          - creation context, license, owner etc: same as for the general sentence object

    - Now, let's find all of the word's translations:
      - Find the first `<table>` following as direct sibling behind an `<h1>` with the content "Meanings"
      - Loop this table's `<tr>`. For each:
        - Get the second `<td>` within the row.
        - In it, there must be the following element:
          - An `<a>` tag. Save the link content as `form_en`
        - There may also be the following two elements:
          - An `<i>` tag. If exists, save as `form_type`
          - Text without a tag between the `<a>` and the `<i>`. If that exists, save as `form_note`.
        - Create a `UnitOfMeaning` for every such row:
          - `text`: `form_en`
          - `language_code`: "en"
          - `pronunciation`: None
          - `type_info`: `form_type` (if exists)
          - `notes`: `form_note` (if exists)
          - `translations`: Add ALL the `UnitOfMeanings` that were created for this word in the previous step!
          - `synonyms`: Add ALL the `UnitOfMeaning`s that were created in relation to this table right here
          - `similar_but_not_synonyms`: []
          - `learning_goals`: None
          - all the license fields: same as the general sentence object

## Misc Features

- Limit of sentences that will be scraped can be set by a constant at the top of the file
