from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book_appointment, name='book'),
    path('my/', views.my_appointments, name='my_list'),
    path('<int:pk>/', views.appointment_detail, name='detail'),
    path('<int:pk>/cancel/', views.cancel_appointment, name='cancel'),
    path('all/', views.all_appointments, name='all_list'),
    path('<int:pk>/update-status/', views.update_appointment_status, name='update_status'),
    path('walk-in/', views.walk_in_appointment, name='walk_in'),
]
