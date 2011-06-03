from django.db import models
from django.core.validators import MaxLengthValidator
import datetime

class record(models.Model):
    url = models.CharField(max_length = 15, primary_key = True, unique = True)
    name = models.CharField(max_length = 100)
    title = models.CharField(max_length = 100)
    text = models.TextField(validators = [MaxLengthValidator(100000)])
    exp_date = models.DateTimeField('expiration time')

    @classmethod
    def rem_old_records(self):
        self.objects.filter(exp_date__lte = datetime.date.today()).delete()
