from django.db import models


# Create your models here.

class Anexo(models.Model):
    nome = models.CharField(max_length=64)
    data = models.DateTimeField(auto_now_add=True)
    arquivo = models.FileField(upload_to='planilha/',)
