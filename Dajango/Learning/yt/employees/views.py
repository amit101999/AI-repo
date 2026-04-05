from django.shortcuts import render
from Emp

# Create your views here.

def employee_list(request):
    emp = Employee.objects.all()
    context = {
        'employees': emp
    }
    return render(request, 'employee_list.html', context)


def employee_detail(request, pk):
    try:
        return httpResponse(f"Employee Detail: {pk}")
    except Employee.DoesNotExist:
        return httpResponse("Employee not found", status=404)