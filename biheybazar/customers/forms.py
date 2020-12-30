from django import forms
from django.db.models import fields
from django.forms import ModelForm, PasswordInput, CharField, Form
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from customers.models import Customer
from users.models import User





class RecommendationForm(ModelForm):
    '''recommendation forms contains two fields, location and culture'''

    class Meta:
        model= Customer
        fields=('location','culture')

    # def __init__(self, *args, **kwargs):
    #     self.customer = kwargs.pop('customer')
    #     super().__init__(*args, **kwargs)
    
    # def save(self):
    #     print(self.customer)
    #     self.customer.location = self.cleaned_data['location']
    #     self.customer.culture=self.cleaned_data['culture']
    #     # form = super(RecommendationForm, self).save()
    #     # print(form)
    #     return self.customer

class ChangeProfilePicForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('profile_pic',)

    def save(self, customer):
        customer.profile_pic = self.cleaned_data['profile_pic']
        customer.save()

class ChangePasswordForm(Form):
    old_password = CharField(widget=PasswordInput)
    new_password = CharField(widget=PasswordInput, validators=[validate_password])
    confirm_password = CharField(widget=PasswordInput)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        new_password = cleaned_data.get('new_password')
    
        if new_password != confirm_password:
            self.add_error('confirm_password', 'Password does not match.')

    def save(self, user):
        if user.check_password(self.cleaned_data['old_password']):
            user.set_password(self.cleaned_data['new_password'])
            user.save()