from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Min, Max
from doctors.models import Doctor

class ChatbotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        message = request.data.get('message', '').lower()
        response_text = ""

        # Basic Intents
        if "hello" in message or "hi" in message or "hey" in message:
            response_text = "Hello! I am the DocConnect Assistant. I can help you find a doctor, check consultation fees, or guide you to book an appointment. How can I assist you today?"
            
        elif "emergency" in message or "urgent" in message or "911" in message or "help me" in message:
            response_text = "<strong class='text-danger'>If this is a medical emergency, please call 911 or visit the nearest emergency room immediately!</strong> DocConnect is for scheduling standard consultations."
        
        elif "cancel" in message or "change" in message or "reschedule" in message:
            response_text = "To cancel or reschedule an appointment, please log in and visit your <a href='patient-dashboard.html'>Patient Dashboard</a>. You can manage all your active bookings there."

        elif "price" in message or "fee" in message or "cost" in message or "charge" in message:
            # Dynamically query the database for fees
            fee_stats = Doctor.objects.aggregate(min_fee=Min('consultation_fee'), max_fee=Max('consultation_fee'))
            min_fee = fee_stats.get('min_fee')
            max_fee = fee_stats.get('max_fee')
            
            if min_fee is not None and max_fee is not None:
                if min_fee == max_fee:
                    response_text = f"The standard consultation fee for our doctors is <strong>₹{min_fee}</strong>. You can check individual doctor profiles on our <a href='doctors.html'>Doctors page</a>."
                else:
                    response_text = f"Consultation fees vary depending on the doctor's specialization and experience. Currently, our fees range from <strong>₹{min_fee} to ₹{max_fee}</strong>. You can check individual profiles for exact fees."
            else:
                response_text = "Consultation fees vary depending on the doctor. You can check individual doctor profiles on our Doctors page for exact fees."
        
        elif "best doctor" in message or "top rated" in message or "highest rated" in message or "good doctor" in message:
            top_doc = Doctor.objects.order_by('-rating').first()
            if top_doc:
                response_text = f"All our doctors are excellent, but currently our highest-rated doctor is <strong>Dr. {top_doc.full_name}</strong> ({top_doc.specialization}) with a brilliant rating of {top_doc.rating}/5! Consultation fee: ₹{top_doc.consultation_fee}."
            else:
                response_text = "You can sort our <a href='doctors.html'>Doctors directory</a> by 'Highest Rated' to find the perfect specialist for you!"

        # Check if the user is asking for a specific specialization dynamically
        else:
            # A dictionary of common keywords mapping to DB specializations
            specialization_keywords = {
                'heart': 'cardio', 'cardio': 'cardio',
                'skin': 'derm', 'derm': 'derm',
                'kid': 'pediatric', 'child': 'pediatric', 'pediatric': 'pediatric',
                'bone': 'ortho', 'joint': 'ortho', 'ortho': 'ortho',
                'nerve': 'neuro', 'brain': 'neuro', 'neuro': 'neuro',
                'eye': 'ophthalmology', 'vision': 'ophthalmology',
                'tooth': 'dentist', 'teeth': 'dentist', 'dentist': 'dentist',
                'mental': 'psychiatrist', 'therapy': 'psychiatrist', 'psychiatrist': 'psychiatrist',
                'stomach': 'gastro', 'digestion': 'gastro'
            }
            
            found_specialization = None
            for kw, spec in specialization_keywords.items():
                if kw in message:
                    found_specialization = spec
                    break
                    
            if found_specialization:
                docs = Doctor.objects.filter(specialization__icontains=found_specialization)
                if docs.exists():
                    names = ", ".join([f"<strong>Dr. {d.full_name}</strong> (₹{d.consultation_fee})" for d in docs])
                    response_text = f"We found the following specialists matching your query: {names}. You can find them in the <a href='doctors.html'>Doctors directory</a> to book a consultation."
                else:
                    response_text = f"We currently don't have any specialists available for that condition right now. Please check back later!"
            else:
                # Try to see if they are asking for a specific doctor by name
                doctor_found = False
                for doc in Doctor.objects.all():
                    if doc.full_name.lower() in message:
                        response_text = f"<strong>Dr. {doc.full_name}</strong> is a great choice! They specialize in {doc.specialization} and their consultation fee is ₹{doc.consultation_fee}. You can click <a href='appointment.html'>here to book an appointment</a> with them."
                        doctor_found = True
                        break
                        
                if not doctor_found:
                    if "book" in message or "appointment" in message or "schedule" in message:
                        response_text = "To book an appointment, you can visit our <a href='appointment.html'>Booking Page</a>. You'll need to select a doctor and choose an available time slot."
                    elif "register" in message or "sign up" in message or "create account" in message:
                        response_text = "You can join DocConnect in seconds! Just head over to our <a href='signup.html'>Sign Up page</a> to create a free patient account."
                    elif "help" in message:
                        response_text = "I can help you with:<br>1. Finding fees (e.g. 'What is the cost?')<br>2. Finding a specialist (e.g. 'I need a heart doctor')<br>3. Doctor exact name lookup."
                    else:
                        response_text = "I'm still learning! While I might not understand everything yet, you can try asking me <strong>'What are your fees?'</strong> or <strong>'Find a heart doctor'</strong>."

        return Response({"reply": response_text})
