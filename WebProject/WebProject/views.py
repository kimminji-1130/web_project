from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    data = 'Main page rendered from template'
    context = {'message': data}
    return render(request, 'index.html', context)