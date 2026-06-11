from django.urls import path
from . import views

app_name = 'candidates'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.my_profile, name='my_profile'),
    path('list/', views.candidate_list, name='list'),
    path('create/', views.receptionist_create_candidate, name='create'),
    path('<int:pk>/', views.candidate_detail, name='detail'),
    path('<int:pk>/edit/', views.edit_candidate, name='edit'),
]

