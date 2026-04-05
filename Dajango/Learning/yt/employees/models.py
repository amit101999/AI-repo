from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    image = models.ImageField(upload_to='employee_images/')

    def __str__(self):
        return self.name