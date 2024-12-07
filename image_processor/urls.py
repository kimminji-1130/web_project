from django.urls import path
from . import views
from .views import PostMemberView
app_name = 'image_processor'

urlpatterns = [
    path('ex01/', views.ex01, name='ex01'),  # 실시간 관제 템플릿
     path('main/', views.main, name='main'),  # 메인 템플릿
    path('analysis/', views.analysis, name='analysis'),  # 분석 템플릿
    path('detection/', views.detection, name='detection'),  # 탐지 템플릿
    path('save-detection/', views.save_detection, name='save_detection'),  # 데이터 저장 API
    path('get-detections/', views.get_detections, name='get_detections'),  # 데이터 가져오기 API
    path('postMember/', PostMemberView.as_view(), name='post_member'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
