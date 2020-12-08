from django import forms
from reviews.models import Review
from vendors.models import Vendor
from customers.models import Customer
 


#============= all the forms of reviews app goes here======#
class ReviewForm(forms.ModelForm):
    """this form contains the fields ratings and description """
    
    class Meta():
        model = Review
        fields = ('ratings','description')

        widgets={
            'description':forms.Textarea(attrs={ 'class':"review-text"})
            }

    def __init__(self,*args,**kwargs):
        vendor = kwargs.pop('vendor')
        customer = kwargs.pop('customer')
        super().__init__(*args,**kwargs)
        self.vendor_obj=Vendor.objects.filter(user__username=vendor).first()
        self.customer_obj=Customer.objects.filter(user__username=customer).first()

    def save(self):
        review = Review.objects.create(ratings=self.cleaned_data['ratings'],
        description=self.cleaned_data['description'],
        customer =self.customer_obj,
        vendor = self.vendor_obj
        )

        return review


        
        

