from django.db import models

# Create your models here.

class lecturas(models.Model):
    id = models.AutoField(primary_key=True)
    ts = models.DateTimeField(auto_now_add=True)
    caja1 = models.CharField(max_length=12 )
    payload = models.CharField(max_length=20)

    def __str__(self):
        return f"Lectura {self.id} - ts: {self.ts} - caja1: {self.caja1} - payload: {self.payload}"
    
    