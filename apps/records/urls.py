from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('my/', views.my_record, name='my_record'),
    path('edit/<int:candidate_pk>/', views.edit_record, name='edit'),
]
