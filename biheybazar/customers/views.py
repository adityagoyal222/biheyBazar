from django.shortcuts import render
from django.views.generic import (UpdateView, FormView)
from customers.models import Customer
from customers.forms import RecommendationForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class Questions(LoginRequiredMixin,FormView):
    '''CBV to ask questions to customer and store the answers in location and culture field of Customer model '''
    model = Customer
    template_name='customers/questions.html'
    # login_url ='/login/'
    form_class = RecommendationForm
    success_url='/'


    #check the validation of Recommendation form
    def form_valid(self,form):
        customer=Customer.objects.filter(user=self.request.user).first()
        recommend_form=form.save(commit=False)
        form.instance.location=form.cleaned_data['location']
        form.instance.culture=form.cleaned_data['culture']
        if recommend_form.user_id is None:
            recommend_form.user_id=self.request.user.id

        form.save()

        return super().form_valid(form)

    # def post(self,request,*args,**kwargs):
    #     # self.object = self.get_object()
    #     customer=Customer.objects.filter(user=self.request.user).first()
    #     context={}
    #     if 'form' in request.POST:
    #         recommend_form=RecommendationForm(request.POST)
    #         print(recommend_form.cleaned_data['location','culture'])
    #         if recommend_form.is_valid():

    #             recommendations=recommend_form.save(commit=False)
    #             recommendations.location=recommend_form.cleaned_data['location']
    #             recommendations.culture=recommend_form.cleaned_data['culture']
    #             recommendations.save()

    #         else:
    #             context['form']=recommend_form

    #     return render(request,self.template_name,self.get_context_data(**context))

    # def get_form_kwargs(self, **kwargs):
    #     kwargs = super().get_form_kwargs()
    #     # print( Customer.objects.filter(user=self.request.user).first())
    #     kwargs['customer'] = Customer.objects.filter(user=self.request.user).first()
    #     return kwargs






   

