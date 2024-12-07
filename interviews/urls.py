from django.urls import path
from .views import RegisterCandidate, RegisterInterviewer, GetAvailableSlots

urlpatterns = [
    path('register_candidate/', RegisterCandidate.as_view(), name='register_candidate'),
    path('register_interviewer/', RegisterInterviewer.as_view(), name='register_interviewer'),
    path('get_available_slots/', GetAvailableSlots.as_view(), name='get_available_slots'),

]
