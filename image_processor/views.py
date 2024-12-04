from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Detection


# 기존 템플릿 렌더링 뷰
def ex01(request):
    return render(request, 'ex01.html')  # 실시간 관제 템플릿 렌더링

def main(request):
    return render(request, 'main.html')  # 메인 템플릿 렌더링

def analysis(request):
    return render(request, 'analysis.html')  # 분석 템플릿 렌더링

def detection(request):
    return render(request, 'detection.html')  # 탐지 템플릿 렌더링


# 데이터 저장 API
@csrf_exempt
def save_detection(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 요청 데이터 파싱
            print("Data received:", data)  # 디버그 로그 추가
            timestamp = data['timestamp']
            object_name = data['object_name']
            object_count = data['object_count']

            # 데이터베이스에 저장
            detection = Detection(
                timestamp=timestamp,
                object_name=object_name,
                object_count=object_count
            )
            detection.save()

            print("Data saved successfully!")  # 디버그 로그 추가
            return JsonResponse({'message': 'Detection saved successfully'}, status=200)
        except Exception as e:
            print("Error:", str(e))  # 디버그 로그 추가
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# 데이터 조회 API
def get_detections(request):
    if request.method == 'GET':
        detections = Detection.objects.all().values('timestamp', 'object_name', 'object_count')
        return JsonResponse(list(detections), safe=False, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
