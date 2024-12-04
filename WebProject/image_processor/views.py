from django.shortcuts import render

def ex01(request):
    return render(request, 'ex01.html')  # 실시간 관제 템플릿 렌더링

def main(request):
    return render(request, 'main.html')  # 메인 템플릿 렌더링

def analysis(request):
    return render(request, 'analysis.html')  # 분석 템플릿 렌더링

def detection(request):
    return render(request, 'detection.html')  # 탐지 템플릿 렌더링
