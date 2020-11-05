from django.db import models


# Create your models here.
class Departamento(models.Model):
    name = models.CharField('Nombre', max_length=50)
    shor_name = models.CharField('Nombre corto', max_length=2, unique=True)
    anulate = models.BooleanField('Anulado', default=False)

    class Meta:
        verbose_name = 'Mi Departamento'
        verbose_name_plural = 'Areas de la empresa'
        ordering = ['-name']  # Ordena los registros
        unique_together = ('name', 'shor_name')  # Solo registros unicos

    def __str__(self):
        return f'{self.id} {self.name} {self.shor_name}'
