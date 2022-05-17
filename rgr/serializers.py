from rest_framework import serializers

from .models import Employees, Services, Barbershop, Customer, Order


class EmployeesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Employees
        fields = ('id', 'first_name', 'second_name', 'phone_number', 'work_experience', 'barbershop', 'user',)


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('name', 'price', 'duration_min',)


class BarbershopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbershop
        fields = ('id', 'name', 'address', 'city',)


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Customer
        fields = ('first_name', 'second_name', 'phone_number', 'email',)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('customer', 'barbershop', 'barber', 'service', 'appointment',)
