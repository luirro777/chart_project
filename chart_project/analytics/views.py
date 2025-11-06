from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Sale
import json
from datetime import datetime, timedelta

# Vista 1: TemplateView - Página principal del dashboard
class DashboardView(TemplateView):
    """
    CBV que renderiza el template con el dashboard.    
    """
    template_name = 'analytics/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos estáticos para el template (no para Chart.js)
        context['total_sales'] = Sale.objects.count()        

        total_revenue = Sale.objects.aggregate(
            total=Sum('amount')
        )
        context['total_revenue'] = total_revenue["total"] or 0
        
        # Explicación: get_context_data es el método clave para pasar datos al template
        return context


# Vista 2: View - API simple que retorna JSON para Chart.js
class SalesDataView(View):
    """
    CBV que retorna datos JSON para Chart.js.    
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        # Datos agrupados por categoría para gráfico de barras/dona
        category_data = Sale.objects.values('category').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        )
        
        # Preparar datos en formato Chart.js
        labels = [item['category'] for item in category_data]
        data = [float(item['total_amount']) for item in category_data]
        
        # Explicación: JsonResponse es la forma estándar de Django para JSON
        return JsonResponse({
            'labels': labels,
            'datasets': [{
                'label': 'Ventas por Categoría (€)',
                'data': data,
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                ]
            }]
        })


# Vista 3: ListView con AJAX - Datos temporales
class SalesTrendView(ListView):
    """
    CBV que puede funcionar tanto como HTML como JSON (con ?format=json).    
    """
    model = Sale
    template_name = 'analytics/trend.html'
    context_object_name = 'sales'
    
    def get_queryset(self):
        # Últimos 30 días
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        return Sale.objects.filter(
            date__gte=thirty_days_ago
        ).order_by('date')
    
    def render_to_response(self, context, **response_kwargs):
        # Si se solicita JSON, retornar datos para gráfico de líneas
        if self.request.GET.get('format') == 'json':
            queryset = self.get_queryset()
            
            # Agrupar por fecha y sumar montos
            trend_data = {}
            for sale in queryset:
                date_str = sale.date.strftime('%Y-%m-%d')
                trend_data[date_str] = trend_data.get(date_str, 0) + float(sale.amount)
            
            dates = sorted(trend_data.keys())
            amounts = [trend_data[date] for date in dates]
            
            return JsonResponse({
                'labels': dates,
                'datasets': [{
                    'label': 'Tendencia de Ventas Diarias',
                    'data': amounts,
                    'borderColor': 'rgb(75, 192, 192)',
                    'tension': 0.1
                }]
            })
        
        # Si no, renderizar el template normalmente
        return super().render_to_response(context, **response_kwargs)