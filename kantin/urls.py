from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.manageMenu, name="managemenu"),
    path('tambah-menu/', views.tambahMenu, name="tambah-menu"),
    path('update-menu/', views.updateMenu, name="update-menu"),
    path('delete-menu/', views.deleteMenu, name="delete-menu"),
    path('list_menu/<int:id>', views.list_menu, name="listmenu"),
    path('add-to-cart/<int:menu_id>', views.add_to_cart, name="addToCart")
]
