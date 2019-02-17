from django.db import models

# Create your models here.

class Participant(models.Model):
    '''
    @properties
    - name
    - phone
    - email
    - payment
    - essay
    '''
    participant_name = models.CharField(max_length=30)
    participant_phone = models.CharField(max_length=30)
    participant_email = models.EmailField()

    participant_payment = models.BooleanField(default=False)
    participant_essay = models.TextField(max_length=3000)