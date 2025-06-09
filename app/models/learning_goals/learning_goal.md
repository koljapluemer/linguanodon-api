# LearningGoal

A learning goal represents something that the learner wants to learn or know.

It has the following properties:

- id
- name
- description (optional)
- parents: [] (non-symmetrical, ManyToMany relationship to other `LearningGoal`s)


It also has an author (the user who created it), and two props: `isPublic`, `isAdminApproved`.