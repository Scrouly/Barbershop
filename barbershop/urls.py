"""barbershop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from rgr.views import *

barber_router = routers.SimpleRouter()
barber_router.register(r"barber", BarberViewSet)

user_router = routers.SimpleRouter()
user_router.register(r"user", CustomerViewSet)

order_router = routers.SimpleRouter()
order_router.register(r"barber", OrderViewSet)

barbershop_router = routers.SimpleRouter()
barbershop_router.register(r"barbershop", BarbershopViewSet)

services_router = routers.SimpleRouter()
services_router.register(r"services", ServicesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rgr.urls')),
    path('api/v1/', include(barber_router.urls)),
    path('api/v1/', include(user_router.urls)),
    path('api/v1/', include(order_router.urls)),
    path('api/v1/', include(barbershop_router.urls)),
    path('api/v1/', include(services_router.urls)),
    #    path('api/v1/barber/', BarberAPIList.as_view()),
    #    path('api/v1/barber/<int:pk>/', BarberAPIUpdate.as_view()),
    #    path('api/v1/barberdestroy/<int:pk>/', BarberAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

]
