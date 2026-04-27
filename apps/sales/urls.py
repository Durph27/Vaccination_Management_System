from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.sale_list, name='list'),
    path('my/', views.my_sales, name='my_sales'),
    path('<int:pk>/', views.sale_detail, name='detail'),
]
