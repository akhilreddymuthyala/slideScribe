from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Presentation

@login_required
def dashboard(request):
    presentations = Presentation.objects.filter(user=request.user)
    context = {
        'presentations': presentations,
        'total': presentations.count(),
        'ready': presentations.filter(status='READY').count(),
        'recent': presentations[:6],
    }
    return render(request, 'dashboard.html', context)