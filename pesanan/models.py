from django.db import models

from user.models import User
from kantin.models import Menu

# Create your models here.

class Pesanan(models.Model):
    STATUS_CHOICES = [
        ('Diterima', 'Diterima'),
        ('Diproses', 'Diproses'),
        ('Selesai', 'Selesai'),
    ]
    
    STATUS_PESANAN= [
        ('Aktif', 'Aktif'),
        ('NonAktif', 'NonAktif'),
    ]
    
    pembeli = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pesanan_pembeli')
    status_cart = models.CharField(max_length=10, choices=STATUS_PESANAN, default="Aktif")
    jumlah_pesanan = models.PositiveIntegerField(default=0)
    total_harga = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Diterima')

class Keranjang(models.Model):
    pesanan = models.ForeignKey(Pesanan, on_delete=models.CASCADE)
    penjual = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Kantin')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    jumlah_pesanan = models.PositiveIntegerField(default=1)
    
    class Meta:
        db_table = "Keranjang"

    def __str__(self):
        return f"{self.menu}'s Keranjang - {self.pembeli}"

