import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docconnect_backend.settings')
django.setup()

from users.models import User
from doctors.models import Doctor, DoctorAvailability

# Create sample doctors
doctors_data = [
    {
        "email": "dr.johnson@docconnect.com",
        "first_name": "Robert",
        "last_name": "Johnson",
        "password": "Doctor123",
        "specialization": "cardiologist",
        "qualification": "MBBS, MD (Cardiology)",
        "experience_years": 15,
        "clinic_address": "123 Heart Care Center, New York",
        "consultation_fee": 150.00,
        "about": "Expert cardiologist with 15 years of experience in heart diseases."
    },
    {
        "email": "dr.sarah@docconnect.com",
        "first_name": "Sarah",
        "last_name": "Williams",
        "password": "Doctor123",
        "specialization": "dermatologist",
        "qualification": "MBBS, MD (Dermatology)",
        "experience_years": 10,
        "clinic_address": "456 Skin Clinic, Los Angeles",
        "consultation_fee": 100.00,
        "about": "Specialized in treating skin conditions and cosmetic dermatology."
    },
    {
        "email": "dr.michael@docconnect.com",
        "first_name": "Michael",
        "last_name": "Chen",
        "password": "Doctor123",
        "specialization": "general",
        "qualification": "MBBS, MD",
        "experience_years": 20,
        "clinic_address": "789 General Hospital, Chicago",
        "consultation_fee": 80.00,
        "about": "Experienced general physician treating various common illnesses."
    },
    {
        "email": "dr.emily@docconnect.com",
        "first_name": "Emily",
        "last_name": "Brown",
        "password": "Doctor123",
        "specialization": "pediatrician",
        "qualification": "MBBS, MD (Pediatrics)",
        "experience_years": 8,
        "clinic_address": "321 Kids Care, Houston",
        "consultation_fee": 120.00,
        "about": "Specialized in child healthcare and pediatric diseases."
    },
    {
        "email": "dr.david@docconnect.com",
        "first_name": "David",
        "last_name": "Lee",
        "password": "Doctor123",
        "specialization": "orthopedic",
        "qualification": "MBBS, MS (Orthopedics)",
        "experience_years": 12,
        "clinic_address": "654 Bone & Joint Center, Miami",
        "consultation_fee": 180.00,
        "about": "Expert in bone and joint surgeries with 12 years of experience."
    }
]

print("Creating sample doctors...")
for doc_data in doctors_data:
    # Create user
    user, created = User.objects.get_or_create(
        email=doc_data['email'],
        defaults={
            'first_name': doc_data['first_name'],
            'last_name': doc_data['last_name'],
            'role': 'doctor'
        }
    )
    
    if created:
        user.set_password(doc_data['password'])
        user.save()
        print(f"Created user: {user.email}")
    else:
        print(f"User already exists: {user.email}")
    
    # Create or update doctor profile
    doctor, created = Doctor.objects.get_or_create(
        user=user,
        defaults={
            'specialization': doc_data['specialization'],
            'qualification': doc_data['qualification'],
            'experience_years': doc_data['experience_years'],
            'clinic_address': doc_data['clinic_address'],
            'consultation_fee': doc_data['consultation_fee'],
            'about': doc_data['about']
        }
    )
    
    if created:
        print(f"Created doctor profile: Dr. {user.full_name}")
    else:
        print(f"Doctor profile already exists: Dr. {user.full_name}")
    
    # Add availability (Monday to Friday, 9 AM to 5 PM)
    for day in range(5):  # 0-4 = Monday to Friday
        availability, created = DoctorAvailability.objects.get_or_create(
            doctor=doctor,
            day_of_week=day,
            defaults={
                'start_time': '09:00',
                'end_time': '17:00'
            }
        )
        if created:
            print(f"Added availability for {availability.get_day_of_week_display()}")

print("\nSample data creation complete!")
print(f"Total doctors in database: {Doctor.objects.count()}")
