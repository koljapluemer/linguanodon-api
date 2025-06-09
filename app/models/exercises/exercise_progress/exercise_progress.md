# ExerciseProgress

A model tracking the learning progress of a `User` regarding a specific `Exercise`

Since we are using `py-fsrs`, we need to represent all props of the fsrs `Card` python class:

```py
card_id: int
state: State
step: int | None
stability: float | None
difficulty: float | None
due: datetime
last_review: datetime | None
```

As regard to `State`, note the class's definition from `ts-fsrs`:

```py
class State(IntEnum):
    """
    Enum representing the learning state of a Card object.
    """

    Learning = 1
    Review = 2
    Relearning = 3
```

Additionally, we are saving the following props:

- `isBlacklisted`