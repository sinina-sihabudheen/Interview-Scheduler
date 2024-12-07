from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, Interviewer, Availability
from .serializers import CandidateSerializer, InterviewerSerializer, AvailabilitySerializer
import logging

logger = logging.getLogger(__name__)

class RegisterCandidate(APIView):
    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterInterviewer(APIView):
    def post(self, request):
        serializer = InterviewerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAvailability(APIView):
    def post(self, request):
        # Register the availability of candidate and interviewer
        candidate_id = request.data.get('candidate_id')
        interviewer_id = request.data.get('interviewer_id')
        interview_slots = request.data.get('interview_slots')

        if not (candidate_id and interviewer_id and interview_slots):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            candidate = Candidate.objects.get(id=candidate_id)
            interviewer = Interviewer.objects.get(id=interviewer_id)
        except Candidate.DoesNotExist or Interviewer.DoesNotExist:
            return Response({"error": "Candidate or Interviewer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create Availability record
        availability = Availability.objects.create(
            candidate=candidate,
            interviewer=interviewer,
            interview_slots=interview_slots
        )

        return Response(AvailabilitySerializer(availability).data, status=status.HTTP_201_CREATED)


class GetAvailableSlots(APIView):
    def get(self, request):
        logger.debug("GetAvailableSlots view called.")

        candidate_id = request.query_params.get('candidate_id')
        interviewer_id = request.query_params.get('interviewer_id')

        if not (candidate_id and interviewer_id):
            return Response({"error": "Both candidate_id and interviewer_id are required.",
                             "received_params": {
                                 "candidate_id": candidate_id,
                                 "interviewer_id": interviewer_id
                             }},
                             status=status.HTTP_400_BAD_REQUEST)

        try:
            candidate = Candidate.objects.get(id=candidate_id)
            interviewer = Interviewer.objects.get(id=interviewer_id)
        except Candidate.DoesNotExist or Interviewer.DoesNotExist:
            return Response({"error": "Invalid candidate or interviewer ID."}, status=status.HTTP_404_NOT_FOUND)

        # Log candidate and interviewer data
        logger.debug(f"Candidate data: {candidate.available_dates}, {candidate.available_times}")
        logger.debug(f"Interviewer data: {interviewer.available_dates}, {interviewer.available_times}")

        # Get availability data for both the candidate and interviewer
        candidate_availabilities = candidate.available_dates
        candidate_times = candidate.available_times

        interviewer_availabilities = interviewer.available_dates
        interviewer_times = interviewer.available_times

        available_slots = []

        # Check for available slots where both have matching available times
        for i, date in enumerate(candidate_availabilities):
            if date in interviewer_availabilities:
                # Check overlapping time slots for this date
                candidate_time_slots = candidate_times[i]
                interviewer_time_slots = interviewer_times[interviewer_availabilities.index(date)]

                logger.debug(f"Matching date: {date}")
                logger.debug(f"Candidate times: {candidate_time_slots}")
                logger.debug(f"Interviewer times: {interviewer_time_slots}")

                for candidate_time in candidate_time_slots:
                    for interviewer_time in interviewer_time_slots:
                        if self.check_time_overlap(candidate_time, interviewer_time):
                            logger.debug(f"Overlap found: Candidate {candidate_time}, Interviewer {interviewer_time}")

                            available_slots.append({"date": date, "time": candidate_time})

        if not available_slots:
            logger.debug("No available slots found.")
            return Response({"error": "No available slots found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"available_slots": available_slots}, status=status.HTTP_200_OK)

    def check_time_overlap(self, candidate_time, interviewer_time):
        # Ensure that both timeslot is exactly 1 hour long
        candidate_start, candidate_end = self.parse_time_range(candidate_time)
        interviewer_start, interviewer_end = self.parse_time_range(interviewer_time)

        # Convert times to minutes for simpler comparison
        candidate_start_minutes = self.time_to_minutes(candidate_start)
        candidate_end_minutes = self.time_to_minutes(candidate_end)
        interviewer_start_minutes = self.time_to_minutes(interviewer_start)
        interviewer_end_minutes = self.time_to_minutes(interviewer_end)

        # Check for exact 1-hour overlap
        return (
            candidate_start_minutes == interviewer_start_minutes and
            candidate_end_minutes == interviewer_end_minutes
        )

    def parse_time_range(self, time_range):
        # Ensure time_range is split correctly into start and end times
        try:
            start_time, end_time = time_range.split("-")
            return start_time, end_time
        except ValueError:
            logger.error(f"Invalid time range format: {time_range}. Expected 'HH:MM-HH:MM'.")
            raise ValueError(f"Invalid time range format: {time_range}. Expected 'HH:MM-HH:MM'.")

    def time_to_minutes(self, time_str):
        try:
            # Split the time string into hours and minutes
            hours, minutes = map(int, time_str.split(":"))
            return hours * 60 + minutes
        except ValueError:
            logger.error(f"Invalid time format: {time_str}. Expected 'HH:MM'.")
            raise ValueError(f"Invalid time format: {time_str}. Expected 'HH:MM'.")
