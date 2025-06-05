# Making JSON Files from Models

1. Get all `LearningGoal`s that have at least 3 related `UnitOfMeaning`.
2. For each, make a JSON file (write to disk, it's a local app)
   1. contain all of `LearningGoal`'s props, like name
   2. contain all related `UnitOfMeanings` in an array, including all their fields (which includes arrays of other `UnitOfMeanings`)
3. Also, create an index file that lists all learning goal's ids and names