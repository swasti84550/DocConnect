from rest_framework import serializers
from datetime import date
from .models import Doctor, DoctorAvailability
from users.serializers import UserProfileSerializer

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ['id', 'day_of_week', 'start_time', 'end_time', 'is_available']

class DoctorSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    availabilities = DoctorAvailabilitySerializer(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'full_name', 'specialization', 'specialization_display', 
                  'qualification', 'experience_years', 'clinic_address', 'consultation_fee', 
                  'about', 'rating', 'total_reviews', 'is_available', 'availabilities']
        read_only_fields = ['rating', 'total_reviews']

class DoctorListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    availabilities = DoctorAvailabilitySerializer(many=True, read_only=True)
    is_available_today = serializers.SerializerMethodField()

    def get_is_available_today(self, obj):
        if not obj.is_available:
            return False
        today_dow = date.today().weekday()  # 0=Monday ... 6=Sunday
        avail = obj.availabilities.filter(day_of_week=today_dow).first()
        if avail:
            return avail.is_available
        return False

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'full_name', 'specialization', 'specialization_display',
                  'qualification', 'experience_years', 'consultation_fee',
                  'rating', 'total_reviews', 'is_available', 'is_available_today', 'availabilities']

class DoctorProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['specialization', 'qualification', 'experience_years', 'clinic_address', 
                  'consultation_fee', 'about', 'is_available']
