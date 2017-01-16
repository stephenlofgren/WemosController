from django.shortcuts import render

# Create your views here.

def lights(request):
    return render(request, "Manage/Lights.html")