from django.db import models

from user.models import User
from kantin.models import Menu

# Create your models here.
class Keranjang(models.Model):
    pembeli = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Mahasiswa')
    penjual = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Kantin')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField(default=1)
    
    class Meta:
        db_table="Keranjang"

    def __str__(self):
        return f"{self.menu}'s Keranjang - {self.pembeli}"