from django.db import models

class Sale(models.Model):
    """Modelo para registrar ventas por categoría y fecha"""
    CATEGORY_CHOICES = [
        ('ELEC', 'Electrónica'),
        ('FOOD', 'Alimentos'),
        ('BOOK', 'Libros'),
        ('CLOT', 'Ropa'),
    ]
    
    category = models.CharField(
        max_length=4, 
        choices=CATEGORY_CHOICES,
        verbose_name='Categoría'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Monto (€)'
    )
    date = models.DateField(verbose_name='Fecha')
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return f"{self.get_category_display()} - {self.amount}€ ({self.date})"