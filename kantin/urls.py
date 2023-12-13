from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.manageMenu, name="managemenu"),
    path('tambah-menu/', views.tambahMenu, name="tambah-menu"),
    path('update-menu/', views.updateMenu, name="update-menu"),
    path('delete-menu/', views.deleteMenu, name="delete-menu"),
    path('list_menu/<int:kantin_id>', views.list_menu, name="listmenu"),
    path('add_to_cart/<int:kantin_id>/<int:menu_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart, name="cart"),
    path('delete-menu/<int:menu_id>', views.hapusMenuCart, name="hapusMenuCart")

]
