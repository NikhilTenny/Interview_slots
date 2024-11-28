from django.db import models

# Create your models here.

USER_TYPE_CHOICES = [('interviewer', 'Interviewer'), ('candidate', 'Candidate')]

class User(models.Model):
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES)
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class TimeSlots(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_time = models.DateTimeField()
    from_time = models.DateTimeField()

