from django.db import models


class Course(models.Model):
    class Difficulty(models.IntegerChoices):
        BEGINNER = 0, 'Beginner'
        INTERMEDIATE = 1, 'Intermediate'
        ADVANCED = 2, 'Advanced'
        FLUENT = 3, 'Fluent'

    title = models.CharField(max_length=255)
    difficulty = models.IntegerField(default=Difficulty.BEGINNER, choices=Difficulty.choices)
    thumbnail = models.FileField(null=False)
    achievement = models.TextField(null=False)
    short_intro = models.CharField(max_length=255, null=False)
    intro = models.TextField()
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'tutor': {
                'name': self.tutor.name
            },
            'difficulty': self.get_difficulty_display(),
            'keywords': [keyword.name for keyword in self.keyword_set.all()]
        }
