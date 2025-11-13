from django.db import models
from singup.models import Patients
from doctor.models import Doctor

class Appointment(models.Model):
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    pid = models.ForeignKey(Patients,on_delete=models.CASCADE)
    docid = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    is_attend = models.BooleanField(default=False)