"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
    
# ]


# urls.py
# urls.py
from django.contrib import admin
from django.urls import path
import uuid
from base.views import manageDevices , DeviceDetailOrDeleteView, ReadingListView,DeviceGraphView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/devices/', manageDevices, name='device-list-create'),
    path('api/devices/<uuid:pk>/', DeviceDetailOrDeleteView, name='device-retrieve-update-delete'),
    # path('api/devices/<str:device_uid>/readings/<str:parameter>/', ReadingListView.as_view(), name='reading-list'),
    path('api/devices/<str:device_uid>/readings/<str:parameter>/', ReadingListView, name='reading-list'),
    path('devices-graph/', DeviceGraphView, name='device-graph'),
]

