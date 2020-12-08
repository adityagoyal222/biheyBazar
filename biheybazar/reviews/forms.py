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

    # def __init__(self,*args,**kwargs):
    #     vendor = kwargs.pop('vendor')
    #     customer = kwargs.pop('customer')
    #     super().__init__(*args,**kwargs)

    def save(self, vendor, customer):
        review = Review.objects.create(ratings=self.cleaned_data['ratings'],
        description=self.cleaned_data['description'],
        customer = customer,
        vendor = vendor
        )

        return review


        
        

