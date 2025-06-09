# View Flow

This is the core of the app.
The learner rotates through different screens, slowly building up their knowledge base.

A central management function in `flow.py` decides where the user goes next.

For example, the user may do 20 exercises that are due, then improve a `LearningGoal` by adding units of meaning, then specifically do 20 exercises of another `LearningGoal`.

## Flow Logic

- The view maintains a hard-coded list of possible flow screens.
- Usually, a user flow