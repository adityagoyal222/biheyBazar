from django.shortcuts import render
from django.views.generic import (TemplateView)


# Create your views here.


class Questions(TemplateView):
    template_name='customers/questions.html'