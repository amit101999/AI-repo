from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Task

# Create your views here.
def add_task(request):
    if request.method == "POST":
        task = request.POST.get('task')
        task = Task.objects.create(title=task)
    return redirect('home')

def mark_completed(request, pk):

    task = Task.objects.get(pk=pk)
    task.completed = True
    task.save()
    return redirect('home')


def mark_incompleted(request, pk):
    
    task = Task.objects.get(pk=pk)
    task.completed = False
    task.save()
    return redirect('home')



        