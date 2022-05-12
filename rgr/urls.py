from django.urls import path, re_path, include

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('customer/add_data', CustomerInfo.as_view(), name = 'add_data'),
    path('customer/change_data', CustomerChange.as_view(), name = 'change_data'),
    path('barber/', view_all_barber, name = 'barber_list'),
    path('add_barber/<int:count>/', random_barber, name = 'create_barber'),
    path('barbers/<int:barber_id>/', view_barber, name = 'barber_inf'),
    path('add_barber/', add_barber, name = 'add_barber'),
    path('random_barber/', RandomBarber.as_view(), name = 'random_barber'),

]