from rest_framework import serializers
from .models import Candidate, Interviewer, Availability

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'email', 'available_dates', 'available_times']


class InterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interviewer
        fields = ['id', 'name', 'email', 'available_dates', 'available_times']


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'candidate', 'interviewer', 'interview_slots']



