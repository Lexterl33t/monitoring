from django.db import models
from django.core.validators import MaxValueValidator
# Create your models here.

class Cpu(models.Model):
    date = models.DateTimeField()
    frequency = models.IntegerField()
    percent_usage = models.IntegerField()

class Disks(models.Model):
    date = models.DateTimeField()
    path = models.CharField(max_length=100)
    size = models.FloatField(validators=[MaxValueValidator(10**8)])
    used = models.FloatField(validators=[MaxValueValidator(10**8)])
    free = models.FloatField(validators=[MaxValueValidator(10**8)])
    percent_used = models.IntegerField()
    current_write_speed = models.FloatField(validators=[MaxValueValidator(10**8)])
    current_read_speed = models.FloatField(validators=[MaxValueValidator(10**8)])

class Ram(models.Model):
    date = models.DateTimeField()
    type = models.CharField(max_length=50)
    used = models.FloatField(validators=[MaxValueValidator(10**8)])
    percent_used = models.FloatField(validators=[MaxValueValidator(10**8)])

