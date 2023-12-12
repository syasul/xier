from django.db import models

from user.models import User
from kantin.models import Menu

# Create your models here.
class Keranjang(models.Model):
    pembeli = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Mahasiswa')
    penjual = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Kantin')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    jumlah_pesanan = models.PositiveIntegerField(default=1)
    
    class Meta:
        db_table="Keranjang"

    def __str__(self):
        return f"{self.menu}'s Keranjang - {self.pembeli}"

class Pesanan(models.Model):
    STATUS_CHOICES = [
        ('Diterima', 'Diterima'),
        ('Diproses', 'Diproses'),
        ('Selesai', 'Selesai'),
    ]
    penjual = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Kantin')
    pembeli = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Mahasiswa')
    keranjang = models.ForeignKey(Keranjang, on_delete=models.CASCADE)
    jumlah_pesanan = models.PositiveIntegerField()
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Diterima')