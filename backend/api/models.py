from django.db import models

# Create your models here.

class Exercise(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    # difficulty level set choices
    class DifficultyLevel(models.IntegerChoices):
        EASY = 1,
        MEDIUM = 2,
        HARD = 3,

    difficuly_rating = models.IntegerField(choices=DifficultyLevel.choices, default=DifficultyLevel.EASY)
    weight = models.IntegerField()


class Workout(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    date = models.DateField()
    exercises = models.ManyToManyField(Exercise, through="Plan")
    completed = models.BooleanField(default=False)


class Plan(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    reps = models.IntegerField()
    sets = models.IntegerField()
