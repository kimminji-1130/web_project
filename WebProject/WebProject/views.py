from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("PBL 프로젝트")