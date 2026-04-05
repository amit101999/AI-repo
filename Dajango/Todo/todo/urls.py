from django.urls import path
from . import views

urlpatterns = [
    path('addtask/', views.add_task, name='add_task'),  # Add this line'home'),
    path('markcompleted/<int:pk>/', views.mark_completed, name='mark_completed'),
    path('markincompleted/<int:pk>/', views.mark_incompleted, name='mark_incompleted'),
]