from django.urls import path
from . import views

app_name = 'image_processor'

urlpatterns = [
    path('ex01/', views.ex01, name='ex01'),
    path('main/', views.main, name='main'),
    path('analysis/', views.analysis, name='analysis'),
    path('detection/', views.detection, name='detection'),
    path('save_detection/', views.save_detection, name='save_detection'),
    path('get_detections/', views.get_detections, name='get_detections'),
]