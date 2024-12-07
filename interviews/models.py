from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField  

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    available_dates = models.JSONField()  
    available_times = models.JSONField()  
    def __str__(self):
        return self.name

class Interviewer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    available_dates = models.JSONField()  
    available_times = models.JSONField()  

    def __str__(self):
        return self.name

class Availability(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="availabilities", null=True, blank=True)

    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE, related_name="availabilities",default=1)
    interview_slots = ArrayField(models.CharField(max_length=50), default=list)  

    def __str__(self):
        return f"Availability for {self.candidate.name} with {self.interviewer.name}"


