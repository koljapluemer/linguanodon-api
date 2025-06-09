# Edit Unit of Meanings

A fairly complex piece of UI to dynamically add `UnitOfMeaning`s and their `Translation`s to a `LearningGoal`.

## Features

- We want a dynamic form, so that the learner can add any number of `UnitOfMeaning`s to a `LearningGoal`. We will use a custom template (no `ModelForm` or anything like that) for this. Alpine will provide interaction.
    - Specifically, the form should load with the `UnitOfMeaning` form two times.
    - It should be ensured that at the bottom a new form is added when needed, so that there is always one free form at the bottom of the list
    - A `UnitOfMeaning` form widget can also be removed with a little close icon
- A given `UnitOfMeaning` may hold an arbitrary number of translations. This should work in a similar manner.
    - The row of forms should start with a single row:
        - An input for the language this translation will be in (dropdown)
        - An input for the translation itself
    - As soon as the learner puts text in the translation field, create another such row below
    - Ensure that always one empty row exists
    - Rows may also be removed with a close icon
    - A `UnitOfMeaning` must at least have one non-empty translation to be saved. However, the language does not matter. The user may create `UnitOfMeaning`s with only a translation in their target language, or in their native language. No matter.
- A given `Translation` input row may be expanded via a `<summary>`/`<detail>` function. If it's collapsed, the user can only input content and language. Expanded, the user may als input pronunciation, type_info, notes and license data. There should also be an option "Copy type info from previous note", which hides the type_info field and in the view copies that from the previous field. Similar options should exist for "notes" and for the batch of license information.