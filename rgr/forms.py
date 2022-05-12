from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'second_name', 'phone_number', 'email',)



    # def save(self):
    #     new_customer = Customer.objects.create(first_name=self.cleaned_data['first_name'],
    #                                            second_name=self.cleaned_data['second_name'],
    #                                            phone_number=self.cleaned_data['phone_number'],
    #                                            email=self.cleaned_data['email'], )
    #     return new_customer
