from rest_framework import serializers
from .models import Appointment
from users.serializers import UserProfileSerializer
from doctors.serializers import DoctorListSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserProfileSerializer(read_only=True)
    doctor = DoctorListSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 
                  'status', 'status_display', 'symptoms', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['patient', 'created_at', 'updated_at']

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'symptoms']
    
    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status', 'notes', 'appointment_date', 'appointment_time', 'symptoms']

from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    appointment_details = AppointmentSerializer(source='appointment', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'appointment', 'appointment_details', 'amount', 'status', 'transaction_id', 'created_at']
        read_only_fields = ['created_at']
