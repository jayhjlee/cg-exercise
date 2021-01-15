from django.urls import path
from . import views

urlpatterns = [
  path('getReportTitles', views.get_report_title, name='report_titles')
]