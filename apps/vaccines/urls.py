from django.urls import path
from . import views

app_name = 'vaccines'

urlpatterns = [
    path('', views.vaccine_list, name='list'),
    path('<int:pk>/', views.vaccine_detail, name='detail'),
    path('history/', views.vaccine_history, name='my_history'),
    path('history/<int:candidate_pk>/', views.candidate_vaccine_history, name='candidate_history'),
    path('appointment/<int:appointment_pk>/add/', views.add_vaccine_administration, name='add_administration'),
    path('administration/<int:adm_pk>/update/', views.nurse_update_administration, name='nurse_update'),
]
