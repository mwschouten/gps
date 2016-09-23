from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.


@login_required
def index(request): 
    return render(request, 'index.html')
