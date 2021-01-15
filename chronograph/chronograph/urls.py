from django.urls import path, include

urlpatterns = [
    path('reports/', include('reports.urls'))
]
