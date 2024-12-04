from django.urls import path
from . import views

app_name = 'image_processor'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('ex01/', views.ex01, name='ex01'),
    path('analysis/', views.analysis, name='analysis'),
    path('detection/', views.detection, name='detection'),
]

