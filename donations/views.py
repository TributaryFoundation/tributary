from django.shortcuts import render

def index(request):
    return render(request, 'donations/index.html', {})

def start(request):
    return render(request, 'donations/start.html', {})

def info(request):
    return render(request, 'donations/info.html', {})

def received(request):
    return render(request, 'donations/received.html', {})

def confirmed(request):
    return render(request, 'donations/confirmed.html', {})
