from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
# import pytz
# from logaktifitas.models import Logaktifitas
from kantin.models import Menu
from user.models import User
from pesanan.models import Keranjang
from django.urls import reverse
from django.utils import timezone


date_now = datetime.now()

@login_required
def manageMenu(request):
    if request.user.role != "Kantin":
        return HttpResponse("Anda Bukan User Kantin")

    context = {
        'menu': Menu.objects.filter(author_id=request.user)
    }
    return render(request, 'manageMenu.html', context)

@login_required
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

@login_required
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

@login_required
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

@login_required
def list_menu(request, kantin_id):
    kantin = get_object_or_404(User, pk=kantin_id)
    menus = Menu.objects.filter(author = kantin)
    
    keranjang = Keranjang.objects.filter(penjual=kantin, pembeli=request.user)
    
    return render(request, "listMenu.html", {'menu_list' : menus, 'kantin_id': kantin_id, 'kantin': kantin, 'keranjang': keranjang})

@login_required
def add_to_cart(request, menu_id, kantin_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    pembeli = request.user
    penjual = menu.author
    
    
    keranjang_item, created = Keranjang.objects.get_or_create(pembeli=pembeli, penjual=penjual, menu=menu)

    if not created:
        keranjang_item.jumlah_pesanan += 1
        keranjang_item.save()


    # Redirect ke halaman sebelumnya
    return HttpResponseRedirect(reverse('kantin:listmenu', kwargs={'kantin_id': kantin_id}))

@login_required
def cart(request, kantin_id, pembeli_id):
    carts = Keranjang.objects.filter(penjual = kantin_id, pembeli = pembeli_id)
    
    total_harga_per_baris = [item.jumlah_pesanan * item.menu.price for item in carts]
    
    total_harga_semua_keranjang = sum(total_harga_per_baris)

    return render(request, "cart.html", {'carts': carts, 'overall_total': total_harga_semua_keranjang })

def hapusMenuCart(request, menu_id):
    Keranjang.objects.filter(menu_id=menu_id).delete()
    pembeli = request.user.id
    carts = Keranjang.objects.filter( pembeli = pembeli)
    timestamp = int(timezone.now().timestamp())
    
    return render(request, 'cart.html', {'timestamp':timestamp ,'carts': carts, 'kantin_id':menu_id, 'pembeli_id':pembeli})
    
    


