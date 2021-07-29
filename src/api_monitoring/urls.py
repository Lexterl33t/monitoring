
from django.urls import path
from .views import System_information, Cpu_information, Memory_information, Disk_information

urlpatterns = [
    path('system-info/', System_information.as_view(), name="system_info"),
    path('cpu/', Cpu_information.as_view(), name='cpu_info'),
    path('ram/', Memory_information.as_view(), name='ram_info'),
    path('disks/', Disk_information.as_view(), name='disks_info'),
]