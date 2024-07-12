from django.db import models

# Create your models here.


class UserConfirm(models.Model):
    email = models.EmailField()
    name=models.CharField(max_length=100)
    surname=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    postal_code=models.CharField(max_length=100)
    code = models.CharField(max_length=6)
    token = models.UUIDField()
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
