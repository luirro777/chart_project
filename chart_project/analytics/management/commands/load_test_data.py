"""
Management command para cargar datos de prueba de ventas.
Útil para demostraciones y desarrollo.
"""
from django.core.management.base import BaseCommand
from analytics.models import Sale
from datetime import datetime, timedelta
from django.db import models 
import random

class Command(BaseCommand):
    help = 'Carga datos de prueba de ventas en la base de datos'
    
    def add_arguments(self, parser):
        """Añade argumentos opcionales al comando"""
        parser.add_argument(
            '--records',
            type=int,
            default=100,
            help='Número de registros a crear (por defecto: 100)'
        )
        
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Borra todos los datos existentes antes de cargar'
        )

    def handle(self, *args, **options):
        """Método principal del comando"""
        
        # Opción para limpiar datos existentes
        if options['clean']:
            self.stdout.write(
                self.style.WARNING('⚠️  Borrando datos existentes...')
            )
            Sale.objects.all().delete()
        
        records_to_create = options['records']
        categories = ['ELEC', 'FOOD', 'BOOK', 'CLOT']
        
        self.stdout.write(
            self.style.SUCCESS(f'🚀 Iniciando carga de {records_to_create} registros de prueba...')
        )
        
        # Crear registros
        sales = []
        for i in range(records_to_create):
            # Fecha aleatoria entre hoy y 60 días atrás
            days_ago = random.randint(0, 60)
            sale_date = datetime.now().date() - timedelta(days=days_ago)
            
            sale = Sale(
                category=random.choice(categories),
                amount=round(random.uniform(20.0, 800.0), 2),
                date=sale_date,
                description=f"Venta demo #{i+1}"
            )
            sales.append(sale)
            
            # Mostrar progreso cada 10 registros
            if (i + 1) % 10 == 0:
                self.stdout.write(
                    self.style.HTTP_INFO(f'  → {i + 1}/{records_to_create} registros creados...')
                )
        
        # Bulk create para mejor rendimiento
        Sale.objects.bulk_create(sales)
        
        # Resumen final
        total_sales = Sale.objects.count()
        total_revenue = Sale.objects.aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Carga completada exitosamente!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'📊 Total de ventas: {total_sales} registros')
        )
        self.stdout.write(
            self.style.SUCCESS(f'💰 Ingresos totales: €{total_revenue:,.2f}')
        )