from django.shortcuts import render
from django.http import HttpResponse

def get_report_title(request):
    return HttpResponse("test")
