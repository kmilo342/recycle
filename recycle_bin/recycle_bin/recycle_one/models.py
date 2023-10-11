from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Material(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name='Material',
        unique=True, max_length=128, blank=False, null=False)
    weight = models.DecimalField(
        verbose_name='Peso del material',
        validators=[MinValueValidator(0)],
        max_digits=8,
        decimal_places=3,
        default=Decimal('0.000'),
        help_text='Peso en Kilogramos',
        blank=False, null=False,
        )
    price = models.DecimalField(verbose_name='Precio x Kg',
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Precio por Kilogramo',
        blank=False, null=False,
        )
    creation_date = models.DateTimeField(
        verbose_name='Fecha de creación',
        auto_now_add=True,
        )
    status = models.BooleanField(verbose_name='Activo', default=True)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'

    def __str__(self):
        return f"{self.name}"


class Collection(models.Model):

    id = models.AutoField(primary_key=True)
    material = models.ForeignKey(
        Material,
        related_name='collected',
        blank=False, null=False,
        on_delete=models.CASCADE,
        default= 1
        )
    weight = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name='Cantidad recolectada',
        help_text='Peso en Kilogramos',
        blank=False, null=False,
        )
    fecha = models.DateField(
        verbose_name='Fecha de recolección',
        help_text='Fecha en que se realizó la recolección',
        blank=False,
        null=False,
    )
    hora = models.TimeField(
        verbose_name='Hora de recolección',
        help_text='Hora en que se realizó la recolección',
        blank=False,
        null=False,
    )
    class Meta:
        verbose_name = 'Recoleccion'
        verbose_name_plural = 'Recolecciones'