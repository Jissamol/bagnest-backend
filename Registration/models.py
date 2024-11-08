from django.db import models

# Create your models here.
class userregister(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    email = models.EmailField(max_length=255, unique=True)  # Unique constraint for email
    contact_number = models.CharField(max_length=15)
    def __str__(self):
        return self.name

