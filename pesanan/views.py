from django.shortcuts import render
from user.models import User
from kantin.models import Menu

# Create your views here.

def home(request):
    
    
    context={
        "kantin": User.objects.filter(role="Kantin") 
    }
    return render(request, 'homeMahasiswa.html', context)

def pespesanKeranjangan(request):
    
    return render(request, "pesananUser.html")
    

    
    