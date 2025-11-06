# 📊 Django + Chart.js CBV Dashboard

![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Django 5.0+](https://img.shields.io/badge/Django-5.0+-green.svg)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4+-red.svg)

Proyecto educativo minimalista que integra **Django 5** con **Chart.js 4** usando Vistas Basadas en Clases (CBVs). Perfecto para enseñar patrones MVC, APIs RESTful básicas y visualización de datos en tiempo real. Originalmente pensado para su uso en la materia Práctica Profesionalizante I, de la Tecnicatura Superior en Desarrollo de Software del Instituto Técnico Superior Córdoba.

---

## 🎯 Características

- **3 Vistas Basadas en Clases** fundamentales: `TemplateView`, `ListView` y `View`
- **Endpoints API JSON** sin necesidad de Django REST Framework
- **Gráficos interactivos**: Barras, donas y líneas con Chart.js
- **Carga de datos de prueba** con management command profesional
- **Código 100% explicativo** con comentarios docstring
- **Diseño responsive** con Bootstrap 5

---

## ⚙️ Requisitos

- Python 3.12+
- Django 5.0+
- Navegador moderno (Chrome, Firefox, Edge)

---

## 📦 Instalación

```bash
# 1. Clonar o descargar el proyecto
cd chart_project

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 4. Instalar Django
pip install django

# 5. Aplicar migraciones
cd chart_project
python manage.py makemigrations
python manage.py migrate

# 6. Crear superusuario (opcional)
python manage.py createsuperuser

# 7. Cargar datos de prueba
python manage.py load_test_data --clean --records 150

# 8. Iniciar servidor
python manage.py runserver
```

Accede a **http://127.0.0.1:8000**

---

## 🧪 Comandos útiles

| Comando | Descripción |
|---------|-------------|
| `python manage.py load_test_data` | Carga 100 registros de prueba |
| `python manage.py load_test_data --records 50` | Carga 50 registros |
| `python manage.py load_test_data --clean` | Borra datos antes de cargar |
| `python manage.py load_test_data --help` | Muestra opciones del comando |

---

## 🏗️ Estructura del Proyecto

```
chart_project/
├── analytics/
│   ├── models.py           # Modelo Sale
│   ├── views.py            # 3 CBVs (Dashboard, API, Tendencia)
│   ├── urls.py             # Rutas de la app
│   └── management/
│       └── commands/
│           └── load_test_data.py  # Comando para datos de prueba
│   └── templates/
│       └── analytics/
│           ├── dashboard.html     # Template principal
│           └── trend.html         # Tendencias temporales
├── chart_project/
│   ├── settings.py         # Configuración Django
│   └── urls.py             # URL principal
└── manage.py
```

---

## 🎓 Explicación de Conceptos Clave

### 1. Vistas Basadas en Clases (CBVs)

```python
# TemplateView: Renderiza un template con datos estáticos
class DashboardView(TemplateView):
    template_name = 'analytics/dashboard.html'
    
    def get_context_data(self, **kwargs):
        # Este método pasa variables al template
        context = super().get_context_data(**kwargs)
        context['total_sales'] = Sale.objects.count()
        return context

# View: Retorna JSON puro (API simple)
class SalesDataView(View):
    def get(self, request):
        data = Sale.objects.values('category').annotate(
            total=Sum('amount')
        )
        return JsonResponse({'data': list(data)})

# ListView: Maneja listas de objetos
class SalesTrendView(ListView):
    model = Sale
    template_name = 'analytics/trend.html'
```

### 2. Queryset ORM Avanzado

```python
# .values().annotate() = GROUP BY de SQL
Sale.objects.values('category').annotate(
    total_amount=Sum('amount'),  # Suma por categoría
    count=Count('id')            # Cuenta registros
)
```

### 3. Peticiones AJAX con Chart.js

```javascript
// Paso 1: Django expone endpoint JSON
fetch("/api/sales-by-category/")

// Paso 2: Chart.js consume los datos
.then(response => response.json())
.then(data => {
    new Chart(ctx, {
        type: 'bar',
        data: data  // Datos directos del backend
    });
});
```

---

## 🔌 Endpoints API

| URL | Vista | Descripción |
|-----|-------|-------------|
| `/` | `DashboardView` | Dashboard con gráficos |
| `/api/sales-by-category/` | `SalesDataView` | JSON para gráficos |
| `/trend/` | `SalesTrendView` | Tendencias temporales |
| `/trend/?format=json` | `SalesTrendView` | JSON de tendencias |

---

## 📊 Ejemplos de Gráficos

### Gráfico de Barras (Categorías)
```javascript
// Datos desde /api/sales-by-category/
{
  "labels": ["ELEC", "FOOD", "BOOK", "CLOT"],
  "datasets": [{
    "data": [1250.50, 890.30, 450.00, 675.20]
  }]
}
```

### Gráfico de Líneas (Tendencias)
```javascript
// Datos desde /trend/?format=json
{
  "labels": ["2024-01-01", "2024-01-02", "2024-01-03"],
  "datasets": [{
    "label": "Ventas Diarias",
    "data": [120.50, 200.00, 95.75]
  }]
}
```



---

## 📚 Recursos para Enseñar

- **Canvas**: El elemento HTML donde Chart.js dibuja
- **Fetch API**: JavaScript moderno para llamadas asíncronas
- **Promise**: `.then()` maneja la respuesta asíncrona
- **ORM Django**: Conversación Python ↔ SQL sin escribir SQL
- **Patrón CBV**: Herencia, métodos `get()`/`post()`, `dispatch()`

---

## 📝 Licencia

GPL-3.0 License - Código libre y de código abierto. Puedes usar, modificar y distribuir este proyecto siempre que mantengas la misma licencia.

---

