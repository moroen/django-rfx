from django.db import models

# Create your models here.


class PacketType(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    description = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.description


class Protocol(models.Model):
    description = models.CharField(max_length=100, primary_key=True)
    enabled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.description
