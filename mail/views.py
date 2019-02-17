from django.shortcuts import render
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'mail/index.html', context={})

def _input_email_conf(request):
    # Receive Email Configuration
    pass