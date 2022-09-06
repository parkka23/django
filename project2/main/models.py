from django.db import models

# Create your models here.

class Laptop(models.Model):
    title=models.CharField(max_length=150)
    price=models.DecimalField(max_digits=7,decimal_places=2)
    color=models.CharField(max_length=50)
    description=models.TextField()
    image=models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.title} {self.price}'

    
