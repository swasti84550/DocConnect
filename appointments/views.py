from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Appointment
from .serializers import (AppointmentSerializer, AppointmentCreateSerializer, 
                          AppointmentUpdateSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_appointments(request):
    """
    Get appointments for the logged-in patient
    Returns appointments where the patient is the requester
    """
    user = request.user
    
    if user.role != 'patient':
        return Response(
            {'error': 'This endpoint is for patients only'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get appointments where patient is the one who booked them
    appointments = Appointment.objects.filter(patient=user).order_by('-appointment_date', '-appointment_time')
    
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_appointments(request):
    """
    Get appointments for the logged-in doctor
    Returns appointments where the doctor is the provider
    """
    user = request.user
    
    if user.role != 'doctor':
        return Response(
            {'error': 'This endpoint is for doctors only'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get appointments where doctor is the one conducting them
    appointments = Appointment.objects.filter(doctor__user=user).order_by('-appointment_date', '-appointment_time')
    
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        print("DEBUG: USER:", user)
        print("DEBUG: USER TYPE:", type(user))
        print("DEBUG: USER ROLE:", getattr(user, 'role', 'NO_ROLE'))
        print("DEBUG: IS AUTHENTICATED:", user.is_authenticated)
        
        if user.role == 'doctor':
            queryset = Appointment.objects.filter(doctor__user=user)
            print("DEBUG: DOCTOR QUERYSET COUNT:", queryset.count())
            return queryset
        elif user.role == 'patient':
            queryset = Appointment.objects.filter(patient=user)
            print("DEBUG: PATIENT QUERYSET COUNT:", queryset.count())
            return queryset
        return Appointment.objects.all()

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Appointment.objects.filter(doctor__user=user)
        elif user.role == 'patient':
            return Appointment.objects.filter(patient=user)
        return Appointment.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AppointmentUpdateSerializer
        return AppointmentSerializer
    
    def destroy(self, request, *args, **kwargs):
        appointment = self.get_object()
        if appointment.status != 'pending':
            return Response(
                {'error': 'Can only cancel pending appointments'},
                status=status.HTTP_400_BAD_REQUEST
            )
        appointment.status = 'cancelled'
        appointment.save()
        return Response({'message': 'Appointment cancelled successfully'}, status=status.HTTP_200_OK)

class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

from .models import Payment
from .serializers import PaymentSerializer

class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Payments where the appointment belongs to the logged in patient
        return Payment.objects.filter(appointment__patient=self.request.user)

class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # In a real app, integrate with Stripe or similar here.
        serializer.save()
