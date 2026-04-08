from django.db import models
from users.models import User

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('general', 'General Physician'),
        ('cardiologist', 'Cardiologist'),
        ('dermatologist', 'Dermatologist'),
        ('neurologist', 'Neurologist'),
        ('pediatrician', 'Pediatrician'),
        ('orthopedic', 'Orthopedic Surgeon'),
        ('gynecologist', 'Gynecologist'),
        ('ophthalmologist', 'Ophthalmologist'),
        ('dentist', 'Dentist'),
        ('psychiatrist', 'Psychiatrist'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    qualification = models.CharField(max_length=200)
    experience_years = models.IntegerField()
    clinic_address = models.TextField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    about = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dr. {self.user.full_name} - {self.get_specialization_display()}"
    
    @property
    def full_name(self):
        return self.user.full_name

class DoctorAvailability(models.Model):
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['doctor', 'day_of_week']
    
    def __str__(self):
        return f"{self.doctor} - {self.get_day_of_week_display()}"

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import time

@receiver(post_save, sender=Doctor)
def create_default_availability(sender, instance, created, **kwargs):
    if created:
        # Create a default Monday-Friday 9 AM to 5 PM schedule
        for day in range(7):
            DoctorAvailability.objects.create(
                doctor=instance,
                day_of_week=day,
                start_time=time(9, 0),
                end_time=time(17, 0),
                is_available=True if day < 5 else False # Available Mon-Fri by default
            )
