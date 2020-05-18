"""
Definition of models.
"""

from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    tema = models.CharField(max_length=200)

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)  
    votes = models.IntegerField(default=0)
    Correcta=models.BooleanField()

class User(models.Model):
    email = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)