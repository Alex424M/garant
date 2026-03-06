from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    DEAL_TYPES = [
        ('rent', 'Аренда'),
        ('sale', 'Продажа'),
    ]

    PROPERTY_TYPES = [
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('land', 'Участок'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.CharField(max_length=255)

    deal_type = models.CharField(max_length=10, choices=DEAL_TYPES)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)

    area = models.FloatField()
    rooms = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_first_image(self):
        first_image = self.images.first()
        if first_image:
            return first_image.image.url
        return '/static/images/no-image.jpg'
    
    def __str__(self):
        return self.title

class Image(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='properties/')
    
class Application(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка от {self.name}"
