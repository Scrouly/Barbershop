import random as rm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_list_or_404
from django.views import View

from .data_creation import random_data as dc
from .forms import CustomerForm
from .models import *


@login_required
def index(request):
    num_barbershops = Barbershop.objects.all().count()
    num_citys = City.objects.all().count()

    num_barbers = Employees.objects.all().count()
    num_services = Services.objects.count()

    return render(
        request,
        'barbershop/index.html',
        context={'num_citys': num_citys, 'num_barbershops': num_barbershops, 'num_barbers': num_barbers,
                 'num_services': num_services},
    )


def view_all_barber(request):
    barber_list = Employees.objects.all()
    return render(request, 'barbershop/barber_create.html', context={"barber": barber_list})


def view_barber(request, barber_id: int):
    get_list_or_404(Employees, id=barber_id)
    one_barber = Employees.objects.get(id=barber_id)
    if 'delete' in request.POST:
        one_barber.delete()
        messages.info(
            request, 'Employee successfully fired!')
    return render(request, 'barbershop/barber_create.html', context={"one_barber": one_barber})


def random_barber(request, count: int):
    barbershop_list = Barbershop.objects.all()
    barber_list = []
    new_barber_name = dc.get_name(count)
    work_experience_list = ['day', 'month', 'year']
    for coiffeur in range(len(new_barber_name)):
        barber = Employees.objects.create(first_name=new_barber_name[coiffeur].split(' ')[1],
                                          second_name=new_barber_name[coiffeur].split(' ')[0],
                                          phone_number=dc.get_telephone(),
                                          work_experience=f'{rm.randint(1, 5)} {rm.choice(work_experience_list)}',
                                          barbershop=rm.choice(barbershop_list))
        barber_list.append(barber)
    return render(request, 'barbershop/barber_create.html', context={"barber_list": barber_list})


class RandomBarber(View):
    def get(self, request):
        count = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        return render(request, 'barbershop/create.html', context={"count": count})

    def post(self, request):
        if 'create' in request.POST:
            count = request.POST.get("count")
        return random_barber(request, count)


def add_barber(request):
    barbershop_list = Barbershop.objects.all()
    if 'add' in request.POST:
        first_name = request.POST.get("fist_name")
        second_name = request.POST.get("second_name")
        phone_number = request.POST.get("phone_number")
        barbershop = request.POST.get("barbershop")
        barbershop = Barbershop.objects.get(name=barbershop)
        Employees.objects.create(first_name=first_name, second_name=second_name, phone_number=phone_number,
                                 barbershop=barbershop)
        messages.info(
            request, 'Barber added successfully.', )

    return render(request, 'barbershop/new_barber.html', context={"barbershop_list": barbershop_list})


class CustomerInfo(View):
    def get(self, request):
        form = CustomerForm()
        return render(request, 'barbershop/customer.html', context={"form": form})

    def post(self, request):
        bound_from = CustomerForm(request.POST)

        if bound_from.is_valid():
            new_from = bound_from.save()

        return render(request, 'barbershop/customer.html', context={'form': bound_from})


class CustomerChange(View):
    def get(self, request):
        customer = Customer.objects.get(pk=1)
        form = CustomerForm(instance=customer)
        return render(request, 'barbershop/change_my_info.html', context={"form": form})

    def post(self, request):
        customer = Customer.objects.all().get(pk=1)
        bound_from = CustomerForm(request.POST, instance=customer)

        if bound_from.is_valid():
            new_from = bound_from.save()

        return render(request, 'barbershop/change_my_info.html', context={"form": bound_from})
# Create your views here.
