import random as rm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_list_or_404, redirect
from django.views import View
from rest_framework import viewsets

from .data_creation import random_data as dc
from .forms import CustomerForm
from .models import *
from .permissions import *
from .serializers import *


class BarberViewSet(viewsets.ModelViewSet):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    permission_classes = [IsAdminOrReadOnly]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsUserOrAdmin]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsUserOrAdmin]


class BarbershopViewSet(viewsets.ModelViewSet):
    queryset = Barbershop.objects.all()
    serializer_class = BarbershopSerializer
    permission_classes = [IsAdminOrReadOnly]


class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = [IsAdminOrReadOnly]


# class BarberAPIList(generics.ListCreateAPIView):
#     queryset = Employees.objects.all()
#     serializer_class = EmployeesSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class BarberAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Employees.objects.all()
#     serializer_class = EmployeesSerializer
#     permission_classes = (IsAuthenticated,)
#
# class BarberAPIDestroy(generics.RetrieveDestroyAPIView):
#     queryset = Employees.objects.all()
#     serializer_class = EmployeesSerializer
#     permission_classes = (IsAdminOrReadOnly,)


#
#
# class BarberRUD(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Employees.objects.all()
#     serializer_class = EmployeesSerializer


# class BarberAPIView(APIView):
#     def get(self, request):
#         lst = Employees.objects.all().values()
#         print(lst)
#         return Response({'Employees': list(lst)})
#
#     def post(self, request):
#         post_new = Employees.objects.create(
#             first_name=request.data['first_name'], second_name=request.data['second_name'],
#             phone_number=request.data['phone_number'], barbershop_id=request.data['barbershop']
#         )
#         return Response({'post': model_to_dict(post_new)})


# class BarberAPIView(generics.ListAPIView):
#     queryset = Employees.objects.all()
#     serializer_class = EmployeesSerializer


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


class ChangeBarberInfo(View):
    def get(self, request, barber_id: int):
        get_list_or_404(Employees, id=barber_id)
        one_barber = Employees.objects.get(id=barber_id)
        barbershop_list = Barbershop.objects.all()
        return render(request, 'barbershop/change_barber_info.html', context={"one_barber": one_barber,
                                                                              "barbershop_list": barbershop_list})

    def post(self, request, barber_id: int):
        if 'change' in request.POST:

            first_name = request.POST.get("fist_name")
            second_name = request.POST.get("second_name")
            phone_number = request.POST.get("phone_number")
            barbershop = request.POST.get("barbershop")
            print(barbershop)
            one_barber = Employees.objects.get(id=barber_id)
            barber = Employees.objects.filter(id=barber_id)

            if one_barber.first_name != first_name:
                barber.update(first_name=first_name)
            if one_barber.second_name != second_name:
                barber.update(second_name=second_name)
            if one_barber.phone_number != phone_number:
                barber.update(phone_number=phone_number)
            if one_barber.barbershop != barbershop:
                barbershop = Barbershop.objects.get(name=barbershop)
                barber.update(barbershop=barbershop)

        return redirect(f"/barbers/{barber_id}")


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
