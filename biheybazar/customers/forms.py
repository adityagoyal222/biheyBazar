from django.forms import ModelForm
from customers.models import Customer





class RecommendationForm(ModelForm):
    '''recommendation forms contains two fields, location and culture'''

    class Meta:
        model= Customer
        print("hello")
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

