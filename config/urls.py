from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('dashboard/', include('apps.candidates.urls', namespace='candidates')),
    path('appointments/', include('apps.appointments.urls', namespace='appointments')),
    path('vaccines/', include('apps.vaccines.urls', namespace='vaccines')),
    path('staff/', include('apps.staff.urls', namespace='staff')),
    path('records/', include('apps.records.urls', namespace='records')),
    path('sales/', include('apps.sales.urls', namespace='sales')),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
