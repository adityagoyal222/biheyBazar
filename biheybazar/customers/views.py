from django.shortcuts import render
from django.views.generic import (UpdateView, FormView, DetailView)
from .models import Customer
from .forms import RecommendationForm, ChangeProfilePicForm, ChangePasswordForm
from users.forms import CustomerSignUpForm
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


class CustomerProfile(FormView, DetailView):
    model = Customer
    form_class = CustomerSignUpForm
    template_name = "customers/customers_profile.html"
    def get_context_data(self, **kwargs):
        customer = Customer.objects.filter(user__pk=self.kwargs['pk']).first()
        context = super(CustomerProfile, self).get_context_data(**kwargs)
        context['customer'] = customer
        if 'change_profile_pic_form' not in context:
            context['change_profile_pic_form'] = ChangeProfilePicForm()
        if 'change_password_form' not in context:
            context['change_password_form'] = ChangePasswordForm()
        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        context = {}
        customer = Customer.objects.filter(user__pk=self.kwargs['pk']).first()

        if 'change_profile_pic' in request.POST:
            profile_pic_form = ChangeProfilePicForm(request.POST, request.FILES)
            if profile_pic_form.is_valid():
                profile_pic_form.save(customer=customer)
            else:
                context['change_profile_pic_form'] = profile_pic_form
        elif 'change_password' in request.POST:
            password_form = ChangePasswordForm(request.POST)
            if password_form.is_valid():
                password_form.save(user=customer.user)
            else:
                context['change_password_form'] = password_form
        return render(request, self.template_name, self.get_context_data(**context))
