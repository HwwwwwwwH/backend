from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator


def jaw_direction_path(instance, filename: str):
    case = instance.case
    patient = instance.patient
    return 'jaws/{0}/{1}/{2}'.format(patient.id, case.case_id, filename)


def tooth_direction_path(instance, filename: str):
    case = instance.case
    patient = instance.patient
    return 'teeth/{0}/{1}/{2}'.format(patient.id, case.case_id, filename)


def get_uid():
    uid = str(uuid4())
    return ''.join(uid.split('-'))


# Create your models here.
class Patient(models.Model):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=200)
    birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male', null=True)
    phone = PhoneNumberField(null=True)


class Case(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    case_id = models.IntegerField()


class JawFile(models.Model):
    POSITION_TYPE = [
        ('Maxillar', 'Maxillar'),
        ('Mandibular', 'Mandibular')
    ]
    PROCESS_TYPE = [
        ('Before_Segmentation', 'Before_Segmentation'),
        ('Segmented', 'Segmented')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    position_type = models.CharField(max_length=20, choices=POSITION_TYPE)
    process_type = models.CharField(max_length=20, choices=PROCESS_TYPE)
    file = models.FileField(upload_to=jaw_direction_path)


class ToothFile(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    quadrant_type = models.IntegerField(validators=[MinValueValidator(1),
                                                    MaxValueValidator(4)])
    position_type = models.IntegerField(validators=[MinValueValidator(1),
                                                    MaxValueValidator(7)])
    file = models.FileField(upload_to=tooth_direction_path)
