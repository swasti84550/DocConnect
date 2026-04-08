from django.urls import path
from . import views
from .views import (DoctorListView, DoctorDetailView, DoctorProfileView,
                    DoctorAvailabilityListView, DoctorAvailabilityDetailView)

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('profile/', DoctorProfileView.as_view(), name='doctor-profile'),
    path('availability/', DoctorAvailabilityListView.as_view(), name='doctor-availability-list'),
    path('availability/<int:pk>/', DoctorAvailabilityDetailView.as_view(), name='doctor-availability-detail'),
    path('<int:pk>/booked-slots/', views.doctor_booked_slots, name='doctor-booked-slots'),
]
