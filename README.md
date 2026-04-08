# DocConnect - Smart Healthcare Platform

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0.1-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-336791?logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

DocConnect is a complete full-stack web application designed to seamlessly bridge the gap between patients and doctors. Featuring a Django/PostgreSQL backend alongside a beautiful, premium, and fully-responsive frontend UI, it streamlines medical appointments and digital consultations.

## ✨ Key Features

- **Premium Modern UI**: Built with a curated HSL color palette, modern typography, glassmorphism overlays, and butter-smooth micro-animations.
- **Smart AI Chatbot (Database-Driven)**: A built-in assistant that parses natural language to lookup real-time consultation fees, match dynamic specializations to database entries, and directly link users to specific doctors by name.
- **End-to-End Authentication Flow**: Secure JWT-based registration and login, including role-based routing (Patients vs. Doctors) and full account-deletion logic.
- **Dynamic Dashboards**: Interactive, single-page dashboards for both Doctors and Patients equipped with stats, revenue calculators, and live status toggle.
- **Advanced Appointment Booking**: Full CRUD support for scheduling, confirming, completing, and canceling appointments dynamically.
- **Doctor Profiles & Scheduling**: Specialized profiles where doctors can manage their exact weekly availability, consultation fees, and public biography down to the minute.

---

## 💻 Tech Stack

**Backend:**
- Django 5.0.1
- Django REST Framework 3.14.0
- PostgreSQL (via psycopg2)
- JWT Authentication (djangorestframework-simplejwt)
- django-cors-headers

**Frontend:**
- HTML5 / Vanilla CSS
- Bootstrap 5 (Grid System & Core Components)
- Custom Glassmorphism & Hover Transforms
- AOS Library (Scroll Animations)
- Javascript (Async Fetch API for dynamic interactions)

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL installed and running
- Node.js (Optional, to use `live-server` for frontend serving)

### 1. Backend Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Configuration
Create a PostgreSQL database named `docconnect`.
Copy `.env.example` to `.env` and fill it with your credentials:

```bash
cp .env.example .env
```
Inside `.env`:
```text
DB_NAME=docconnect
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Migrate and Seed Data
```bash
python manage.py makemigrations
python manage.py migrate

# Create your admin credentials
python manage.py createsuperuser

# Optional: Run the included seed script to populate sample doctor data
python create_sample_data.py
```

### 5. Start Servers

**Django Backend:**
```bash
python manage.py runserver
# Runs on http://127.0.0.1:8000
```

**Frontend Server (in a new terminal):**
```bash
npx --yes live-server
# Runs on http://127.0.0.1:8080
```

---

## 📡 Core API Endpoints

### Authentication & Profile
- `POST /api/auth/register/` - Register new patient or doctor
- `POST /api/auth/login/` - Authenticate and yield JWT tokens
- `GET/PUT /api/auth/profile/` - Access base User profile details
- `DELETE /api/auth/profile/` - Permanent account deletion

### AI Chatbot
- `POST /api/chat/` - Natural language query engine (returns dynamic DB-validated responses for doctors, fees, and specializations)

### Doctors Data
- `GET /api/doctors/` - Search and list doctors
- `GET /api/doctors/{id}/` - Detailed lookup
- `GET/PUT /api/doctors/profile/` - Manage specific doctor configurations (experience, bio, fees)
- `GET/POST/PUT /api/doctors/availability/` - Manage weekly active schedules

### Appointments Lifecycle
- `GET /api/appointments/` - Feed of user/doctor appointments
- `POST /api/appointments/create/` - Form a new booking request
- `PATCH /api/appointments/{id}/` - Update status (e.g., `pending` -> `confirmed` | `completed`)

---

## 🗂 Project Structure
```text
DocConnect-1/
├── docconnect_backend/      # Core Django app (Settings, URLs, Chatbot logic)
├── users/                   # Base User model & robust Authentication API
├── doctors/                 # Doctor profiles & availability scheduling API
├── appointments/            # Appointment booking core API models mapped to users
├── js/api.js                # Global frontend wrapper managing REST calls & JWT
├── *.html                   # Rich frontend views (Dashboards, directories, auth)
├── create_sample_data.py    # Database seeder
└── manage.py                # Django CLI
```

## 🔒 Security Best Practices for Deployment
- Switch `DEBUG=False` in `settings.py` before live production.
- Use strong Database credentials and ensure a strong `SECRET_KEY`.
- Run on `HTTPS`.
- Restrict `CORS_ALLOWED_ORIGINS` to your registered frontend domain address.

---

## 👥 User Workflows

### **Patient Workflow**
1. **Discover**: Browse the landing page, chat with the AI Assistant to find doctors by specialty or cost.
2. **Onboard**: Sign up for an account via the unified Auth system.
3. **Book**: Select a doctor, choose an available date/time, and submit your symptoms.
4. **Manage**: Use the Patient Dashboard to view upcoming appointments, check historical records, or cancel bookings if needed. Account deletion is available via the Settings panel.

### **Doctor Workflow**
1. **Onboard & Profile**: Register as a doctor and define your specialty, bio, clinic address, and flat consultation fee.
2. **Manage Schedule**: Toggle active/inactive days of the week and define daily working hours (e.g. 09:00 AM to 05:00 PM).
3. **Process Appointments**: Monitor the Doctor Dashboard metrics. Confirm pending appointments, conduct consultations, and mark as 'Completed'.
4. **Data Privacy**: Permanently wipe all data and profile records via the 'Danger Zone' in Settings.

---

## 🗺 Future Roadmap

- **Video Consultations**: Integrate API for live WebRTC/Twilio video calls for 'Online' labeled appointments.
- **Payment Gateway**: Process consultation fees securely during the booking phase via Stripe or Razorpay.
- **Prescription Generator**: Allow doctors to write and attach PDF prescriptions directly to a completed appointment record.
- **LLM Chatbot Upgrade**: Swap the Regex-driven Chatbot to a fully localized LLM backend using models like OpenAI or Gemini for highly contextual medical triage.

---

## 🤝 Contributing

Contributions to DocConnect are highly encouraged!

1. **Fork** the repository
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request** against the absolute main branch.

> **Note**: For major architectural changes, please open an issue first to discuss what you would like to change. Keep the UI aesthetic strictly tied to the predefined Glassmorphism/Dark HSL palette.

---
*Built with ❤️ for modern healthcare.*
