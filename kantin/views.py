from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
# import pytz
# from logaktifitas.models import Logaktifitas
from kantin.models import Menu
from user.models import User
from pesanan.models import Keranjang
from django.contrib.sessions.models import Session

date_now = datetime.now()

@login_required
def manageMenu(request):
    if request.user.role != "Kantin":
        return HttpResponse("Anda Bukan User Kantin")

    context = {
        'menu': Menu.objects.filter(author_id=request.user)
    }
    return render(request, 'manageMenu.html', context)
    
    

def tambahMenu(request):
    if request.user.role != "Kantin":
        return HttpResponse("Anda Bukan User Kantin")
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        stok = request.POST.get('stok')
        if int(price) < 1:
            return HttpResponse('Minimal harga 1')
        image = request.FILES['image']
        author = request.user

        add_menu_dict = {
            "Name": name,
            "Price": price,
            "Desc": desc,
            "Stok": stok,
            "Author": author.username
        }
        try:
            Menu.objects.create(name=name, price=int(
                price), image=image, desc=desc, stok=stok, author=author)
            # Logaktifitas.objects.create(
            #     pegawai=request.user, activity="Menambahkan Menu %s" % add_menu_dict, date=date_now)

            messages.success(request, 'Success menambah menu baru')
        except:
            messages.error(request, 'Failed menambah menu baru')

    return redirect('kantin:managemenu')

def updateMenu(request):
    if request.user.role != "Kantin":
        return HttpResponse("Anda Bukan User Kantin")
    if request.method == "POST":
        menuID = request.POST.get('id')
        image = request.FILES['image']
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        stok = request.POST.get('stok')
        if int(price) < 1:
            return HttpResponse('Minimal harga 1')
        image = request.FILES['image']

        menu_obj = Menu.objects.get(id=menuID)
        menu_obj.name = name
        menu_obj.price = int(price)
        menu_obj.desc = desc
        menu_obj.stok = stok
        menu_obj.image = image

        update_menu_dict = {
            "menuID": menuID,
            "Name": name,
            "Price": price,
            "Desc": desc,
            "Stok": stok,
            "Author": request.user.username
        }
        print(update_menu_dict)
        try:
            menu_obj.save()
            # Logaktifitas.objects.create(
            #     pegawai=request.user, activity="Mengupdate Menu menjadi %s" % update_menu_dict, date=date_now)
            messages.success(request, 'Success update menu')
        except:
            messages.error(request, 'Failed update menu')

    return redirect('kantin:managemenu')

def deleteMenu(request):
    if request.user.role != "Kantin":
        return HttpResponse("Anda Bukan User Kantin")
    if request.method == "POST":
        try:
            menu_name = Menu.objects.filter(id=request.POST.get('id'))
            print(menu_name)
            Menu.objects.filter(id=request.POST.get('id')).delete()
            # Logaktifitas.objects.create(
            #     pegawai=request.user, activity="Mendelete Menu %s" % menu_name, date=date_now)
            messages.success(request, 'Success delete menu')
        except:
            messages.error(request, 'Failed delete menu')

    return redirect('kantin:managemenu')
    
def list_menu(request, id):
    kantin = get_object_or_404(User, pk=id)
    menus = Menu.objects.filter(author = kantin)
    
    return render(request, "listMenu.html", {'menu_list' : menus})

def add_to_cart(request, id):
    menu = get_object_or_404(Menu, pk=id)
    pembeli = request.user
    penjual = menu.author
    
    
    if request.user.role == 'Mahasiswa':
            keranjang, created = Keranjang.objects.get_or_create(
            menu=menu,
            pembeli=pembeli,
            penjual=penjual,  
            jumlah=request.POST.get('jumlah_pesan', 1)# Ganti dengan atribut penjual yang sesuai
        )
            
    keranjang_list = Keranjang.objects.filter(role="Mahasiswa")

    context = {
        'keranjang_list': keranjang_list,
    }


    # Redirect ke halaman sebelumnya
    return redirect('kantin:addToCart', context)

