from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    code_postal = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

class Book(models.Model):
    title=models.CharField(max_length=150)
    author= models.CharField(max_length=150)
    price=models.FloatField()
    image = models.ImageField(upload_to='books/', blank=True, null=True)
    urlimg = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

class Panier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.book.price * self.quantity

class Commande(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=500)
    date_commande = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)


class CommandeBooks(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_total_price(self):
        return self.book.price * self.quantity
    



