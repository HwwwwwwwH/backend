from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator
from main.storage import FileStorage


def jaw_direction_path(instance, filename: str):
    case = instance.case
    patient = instance.patient
    position_type = instance.position_type
    process_type = instance.process_type
    ext = filename.split('.')[-1]
    file_name = process_type + '_' + position_type + '.' + ext
    return '{0}/{1}/jaws/{2}'.format(patient.id, case.case_count, file_name)


def tooth_direction_path(instance, filename: str):
    case = instance.case
    patient = instance.patient
    ext = filename.split('.')[-1]
    file_name = '{0}{1}'.format(instance.quadrant_type, instance.position_type) + '.' + ext
    return '{0}/{1}/teeth/{2}'.format(patient.id, case.case_count, file_name)


def dicom_direction_path(instance, filename: str):
    case = instance.case
    patient = instance.patient
    return '{0}/{1}/dicoms/{2}'.format(patient.id, case.case_count, filename)


def get_uid():
    uid = str(uuid4())
    return ''.join(uid.split('-'))


def get_case_count(patient):
    return len(Case.objects.filter(patient=patient)) + 1


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
    case_count = models.IntegerField()


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
    file = models.FileField(upload_to=jaw_direction_path, storage=FileStorage())


class ToothFile(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    quadrant_type = models.IntegerField(validators=[MinValueValidator(1),
                                                    MaxValueValidator(4)])
    position_type = models.IntegerField(validators=[MinValueValidator(1),
                                                    MaxValueValidator(8)]) # 8: wisdom tooth
    file = models.FileField(upload_to=tooth_direction_path, storage=FileStorage())
    isExtracted = models.BooleanField(default=False)


class DicomFile(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    file = models.FileField(upload_to=dicom_direction_path, storage=FileStorage())


# quaternion: [x, y, z], angle
class ToothPosition(models.Model):
    tooth = models.ForeignKey(ToothFile, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    angle = models.FloatField()
