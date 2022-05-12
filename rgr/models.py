from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    second_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

    class Meta:
        db_table = 'Customer'


class Order(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, null=True, blank=True)
    barbershop = models.ForeignKey('Barbershop', on_delete=models.CASCADE, null=True, blank=True)
    barber = models.ForeignKey('Employees', on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey('Services', on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.DateTimeField()

    def __str__(self):
        return f"{self.customer} " \
               f"{self.barber} " \
               f"{self.appointment}"

    class Meta:
        db_table = 'Order'


class Barbershop(models.Model):
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=150)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'Barbershop'


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'City'


class Employees(models.Model):
    first_name = models.CharField(max_length=25)
    second_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=30)
    work_experience = models.CharField(max_length=50, default='0 days')
    date_of_employment = models.DateField(default=date.today)
    barbershop = models.ForeignKey('Barbershop', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

    class Meta:
        db_table = 'Employees'

    def get_url(self):
        return reverse('barber_inf', args=[self.id])

class Services(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    duration_min = models.IntegerField()

    def __str__(self):
        return f"{str(self.name)} - {str(self.price)} руб."

    class Meta:
        db_table = 'Services'
