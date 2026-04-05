from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from  .models import Product

# Create your views here.

def home(request):
    return HttpResponse("Hello, World! This is the home page.")

def hello(request):
    return HttpResponse("Hello, World! This is the hello page.")

def templateshome(request):
    context = {
        "name" :"amit" ,
        "age" : 20
    }
    return render(request, 'home.html' , context)


def create_product(request):
    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")

    product = Product.objects.create(
        name="Sample Product test",
        price=9.99,
        description="This is a sample product."
    )
    return HttpResponse(f"Product created")

def get_products(request):
    products = Product.objects.all();
    output = ""

    for product in products:
        output += f"{product.name} - {product.price} <br>"
    return HttpResponse(output)

def update_product(request):
    product = Porducts.objects.get(id=1)
    product.price = 19.99
    product.save()

    return HttpResponse("Product updated")

def delete_product(request):
    product = Product.objects.get(id=1)
    product.delete()

    return HttpResponse("Product Deleted")