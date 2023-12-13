from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from user.models import User
from kantin.models import Menu
from pesanan.models import Keranjang
from pesanan.models import Pesanan

from django.urls import reverse


# Create your views here.

def home(request):
    
    
    context={
        "kantin": User.objects.filter(role="Kantin") 
    }
    return render(request, 'homeMahasiswa.html', context)

def pesanKeranjang(request, pesanan_id):
    user = request.user
    pesanan = get_object_or_404(Pesanan, id=pesanan_id)
    carts = Keranjang.objects.filter(pesanan=pesanan_id)

    total_harga_per_baris = [item.jumlah_pesanan * item.menu.price for item in carts]
    overall_price = sum(total_harga_per_baris)

    pesanan.total_harga = overall_price
    pesanan.jumlah_pesanan = carts.count()
    pesanan.status = 'Diterima'
    pesanan.status_cart = 'NonAktif'
    
    pesanan.save()

    return redirect(reverse('pesanan:pesananUser', kwargs={'pembeli_id': user.id}))
    


def pesananUser(request, pembeli_id):
    
    return render(request, "pesananUser.html")

def pesananAdmin(request):
    return render(request, "pesananAdmin.html")
    
    

    
    