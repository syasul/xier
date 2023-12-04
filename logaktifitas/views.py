from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Logaktifitas

@login_required
def logaktifitas(request):
    if request.user.role != "Admin":
        return HttpResponse("Anda Bukan Admin")
    log = Logaktifitas.objects.all()
    return render(request, 'logaktifitas.html', {'log': log})