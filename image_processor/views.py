from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Detection
from datetime import datetime
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum

def analysis(request):
    # `object_name` 별 데이터 집계
    data = Detection.objects.values('object_name').annotate(total_count=Sum('object_count')).order_by('-total_count')

    # JSON 데이터로 전달할 리스트 생성
    labels = [entry['object_name'] for entry in data]
    counts = [entry['total_count'] for entry in data]

    return render(request, 'analysis.html', {'labels': labels, 'counts': counts})

class PostMemberView(APIView):
    def post(self, request, *args, **kwargs):
        # 요청 데이터 처리 (예: 데이터베이스 저장 등)
        data = request.data
        return Response({'message': 'Member saved successfully!', 'data': data}, status=status.HTTP_201_CREATED)
    
    def get(self, request, *args, **kwargs):
        return Response({'detail': 'Method "GET" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
def dashboard(request):
    # 데이터베이스에서 데이터를 가져옴
    total_recognitions = Detection.objects.aggregate(Sum('object_count'))['object_count__sum'] or 0
    deer_count = Detection.objects.filter(object_name='고라니').aggregate(Sum('object_count'))['object_count__sum'] or 0
    boar_count = Detection.objects.filter(object_name='멧돼지').aggregate(Sum('object_count'))['object_count__sum'] or 0
    bird_count = Detection.objects.filter(object_name='새').aggregate(Sum('object_count'))['object_count__sum'] or 0
    raccoon_count = Detection.objects.filter(object_name='너구리').aggregate(Sum('object_count'))['object_count__sum'] or 0
    people_count = Detection.objects.filter(object_name='사람').aggregate(Sum('object_count'))['object_count__sum'] or 0

    # 데이터를 템플릿으로 전달
    context = {
        'total_recognitions': total_recognitions,
        'deer_count': deer_count,
        'boar_count': boar_count,
        'bird_count': bird_count,
        'raccoon_count': raccoon_count,
        'people_count': people_count,
    }
    return render(request, 'dashboard.html', context)

# 기존 템플릿 렌더링 뷰
def ex01(request):
    return render(request, 'ex01.html')  # 실시간 관제 템플릿 렌더링

def main(request):
    # 데이터베이스에서 객체별 데이터 집계
    data = Detection.objects.values('object_name').annotate(total=Sum('object_count')).order_by('-total')
    labels = [entry['object_name'] for entry in data]
    counts = [entry['total'] for entry in data]

    total_recognitions = sum(counts)
    deer_count = Detection.objects.filter(object_name='고라니').aggregate(total=Sum('object_count'))['total'] or 0
    boar_count = Detection.objects.filter(object_name='멧돼지').aggregate(total=Sum('object_count'))['total'] or 0
    bird_count = Detection.objects.filter(object_name='새').aggregate(total=Sum('object_count'))['total'] or 0
    raccoon_count = Detection.objects.filter(object_name='너구리').aggregate(total=Sum('object_count'))['total'] or 0
    people_count = Detection.objects.filter(object_name='사람').aggregate(total=Sum('object_count'))['total'] or 0

    context = {
        'labels': json.dumps(labels),  # JSON 직렬화
        'counts': json.dumps(counts),  # JSON 직렬화
        'total_recognitions': total_recognitions,
        'deer_count': deer_count,
        'boar_count': boar_count,
        'bird_count': bird_count,
        'raccoon_count': raccoon_count,
        'people_count': people_count,
    }

    return render(request, 'main.html', context)


# 데이터 저장 API
@csrf_exempt
def save_detection(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
            object_name = data['object_name']
            object_count = data['object_count']

            # 데이터베이스에 저장
            Detection.objects.create(
                timestamp=timestamp,
                object_name=object_name,
                object_count=object_count
            )
            return JsonResponse({'message': 'Detection saved successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# 분석 뷰
def analysis(request):
    # 객체별 데이터 집계
    object_counts = Detection.objects.values('object_name').annotate(total_count=Sum('object_count'))

    labels = [obj['object_name'] for obj in object_counts]
    counts = [obj['total_count'] for obj in object_counts]

    context = {
        'labels': labels,
        'counts': counts,
    }
    return render(request, 'analysis.html', context)


# 탐지 내역 뷰
def detection(request):
    detections = Detection.objects.all().order_by('-timestamp')  # 최신 데이터 순서
    return render(request, 'detection.html', {'detections': detections})


# 데이터 반환 API
def get_detections(request):
    if request.method == 'GET':
        detections = Detection.objects.all().order_by('-timestamp')
        data = list(detections.values('timestamp', 'object_name', 'object_count'))
        return JsonResponse({'detections': data}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# 데이터 저장 API
@csrf_exempt
def save_detection(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
            object_name = data['object_name']
            object_count = data['object_count']

            # 데이터베이스에 저장
            Detection.objects.create(
                timestamp=timestamp,
                object_name=object_name,
                object_count=object_count
            )
            return JsonResponse({'message': 'Detection saved successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# 분석 뷰
def analysis(request):
    # 객체별 데이터 집계
    object_counts = Detection.objects.values('object_name').annotate(total_count=Sum('object_count'))

    labels = [obj['object_name'] for obj in object_counts]
    counts = [obj['total_count'] for obj in object_counts]

    context = {
        'labels': labels,
        'counts': counts,
    }
    return render(request, 'analysis.html', context)


# 탐지 내역 뷰
def detection(request):
    detections = Detection.objects.all().order_by('-timestamp')  # 최신 데이터 순서
    return render(request, 'detection.html', {'detections': detections})


# 데이터 반환 API
def get_detections(request):
    if request.method == 'GET':
        detections = Detection.objects.all().order_by('-timestamp')
        data = list(detections.values('timestamp', 'object_name', 'object_count'))
        return JsonResponse({'detections': data}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
def analysis(request):
    # Fetch detections grouped by object_name
    object_summary = Detection.objects.values('object_name').annotate(total_count=Sum('object_count')).order_by('-total_count')

    # Fetch detections grouped by date
    date_summary = Detection.objects.extra(select={'date': "DATE(timestamp)"}).values('date', 'object_name').annotate(total_count=Sum('object_count')).order_by('date')

    # Prepare data for left-side table (object summary)
    left_table = object_summary

    # Prepare data for right-side chart
    chart_labels = []
    chart_data = {}

    for entry in date_summary:
        if entry['date'] not in chart_labels:
            chart_labels.append(entry['date'])

        if entry['object_name'] not in chart_data:
            chart_data[entry['object_name']] = [0] * len(chart_labels)

        chart_data[entry['object_name']][chart_labels.index(entry['date'])] = entry['total_count']

    # Fetch all detections for bottom table
    detections = Detection.objects.all().order_by('-timestamp')

    return render(request, 'analysis.html', {
        'left_table': left_table,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'detections': detections,
    })
def detection(request):
    detections = Detection.objects.all().order_by('-timestamp')  # 최신 데이터 순서로 정렬
    return render(request, 'detection.html', {'detections': detections})  # 데이터를 템플릿으로 전달


def get_detections(request):
    if request.method == 'GET':
        detections = Detection.objects.all().order_by('-timestamp')
        # JSON으로 변환하여 반환
        data = serialize('json', detections)
        return JsonResponse({'detections': data}, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# 데이터 저장 API
@csrf_exempt
def save_detection(request):
    if request.method == 'POST':
        try:
            # JSON 데이터 파싱
            data = json.loads(request.body)
            print("Received POST data:", data)  # 디버깅 로그
            timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
            object_name = data['object_name']
            object_count = data['object_count']

            # 데이터베이스에 저장
            detection = Detection.objects.create(
                timestamp=timestamp,
                object_name=object_name,
                object_count=object_count
            )
            print("Saved to DB:", detection)  # 디버깅 로그

            return JsonResponse({'message': 'Detection saved successfully!'}, status=200)
        except Exception as e:
            print("Error while saving detection:", str(e))  # 디버깅 로그
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
