from django.shortcuts import render
from .models import HK_JYS
# Create your views here.

def J03_01_C_T60(request):
    HK = HK_JYS.objects.all()
    return render(request,'J03_01_C_T60/J03_01_C_T60.html',locals())