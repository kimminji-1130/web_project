from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Detection
from datetime import datetime
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.utils.safestring import mark_safe

def analysis(request):
    # 객체별 데이터 집계
    object_summary = (
        Detection.objects.values('object_name')
        .annotate(total_count=Sum('object_count'))
        .order_by('-total_count')
    )

    # 날짜별 데이터 집계
    date_summary = (
        Detection.objects.extra(select={'date': "DATE(timestamp)"})
        .values('date', 'object_name')
        .annotate(total_count=Sum('object_count'))
        .order_by('date')
    )

    # 차트 데이터를 준비
    chart_labels = []
    chart_data = {}

    for entry in date_summary:
        date = entry['date']
        object_name = entry['object_name']

        # 날짜가 chart_labels에 없으면 추가하고, 모든 객체 데이터 초기화
        if date not in chart_labels:
            chart_labels.append(date)
            for obj_name in chart_data.keys():
                chart_data[obj_name].append(0)

        # 객체 이름 초기화
        if object_name not in chart_data:
            chart_data[object_name] = [0] * len(chart_labels)

        # 날짜 인덱스 가져오기
        index = chart_labels.index(date)

        # 배열의 길이가 부족하면 확장
        if len(chart_data[object_name]) <= index:
            chart_data[object_name].extend([0] * (index + 1 - len(chart_data[object_name])))

        # 데이터 업데이트
        chart_data[object_name][index] = entry['total_count']

    # 모든 객체 이름에 대해 데이터 길이를 동기화 (누락된 날짜 채우기)
    for object_name in chart_data:
        if len(chart_data[object_name]) < len(chart_labels):
            chart_data[object_name] += [0] * (len(chart_labels) - len(chart_data[object_name]))

    # 탐지된 객체 내역
    detections = Detection.objects.all().order_by('-timestamp')

    # 데이터 직렬화 후 템플릿에 전달
    return render(request, 'analysis.html', {
        'left_table': object_summary,
        'chart_labels': mark_safe(json.dumps(chart_labels)),
        'chart_data': mark_safe(json.dumps(chart_data)),
        'detections': detections,
    })

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

# 데이터 반환 API
def get_detections(request):
    if request.method == 'GET':
        detections = Detection.objects.all().order_by('-timestamp')
        data = list(detections.values('timestamp', 'object_name', 'object_count'))
        return JsonResponse({'detections': data}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

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
