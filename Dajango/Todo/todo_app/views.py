
from todo.models import Task

from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    tasks = Task.objects.filter(completed=False).order_by('-created_at')
    completedTask = Task.objects.filter(completed=True).order_by('-created_at')
    context = {
        'tasks': tasks ,
        'completedTask':completedTask,
    }
    return render(request, 'home.html', context)