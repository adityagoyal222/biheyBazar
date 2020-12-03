from django import forms
from reviews.models import Review




#============= all the forms of reviews app goes here======#
class ReviewForm(forms.ModelForm):
    
    class Meta():
        model = Review
        fields = ('ratings','description')

        # description= forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20})


        widgets={
            'description':forms.Textarea(attrs={ 'class':"review-text"})
            }
        

