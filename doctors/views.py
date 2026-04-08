from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Doctor, DoctorAvailability
from .serializers import (DoctorSerializer, DoctorListSerializer, 
                          DoctorProfileUpdateSerializer, DoctorAvailabilitySerializer)

class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorListSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['specialization']
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
    ordering_fields = ['rating', 'consultation_fee', 'experience_years']

class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]

class DoctorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.doctor_profile
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DoctorSerializer
        return DoctorProfileUpdateSerializer

class DoctorAvailabilityListView(generics.ListCreateAPIView):
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.request.user.doctor_profile.availabilities.all()
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor_profile)

class DoctorAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.request.user.doctor_profile.availabilities.all()

from appointments.models import Appointment
from datetime import datetime

@api_view(['GET'])
@permission_classes([AllowAny])
def doctor_booked_slots(request, pk):
    date_str = request.query_params.get('date')
    if not date_str:
        return Response({"error": "date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Fetch active appointments for the given doctor and date
    appointments = Appointment.objects.filter(
        doctor_id=pk, 
        appointment_date=date_obj
    ).exclude(status__in=['cancelled', 'no_show'])
    
    # Format to match frontend generation (HH:MM)
    booked_times = [appt.appointment_time.strftime("%H:%M") for appt in appointments]
    
    return Response({"booked_slots": booked_times})
