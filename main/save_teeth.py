from pathlib import Path
from main.models import Patient, Case, ToothFile
from django.core.files import File
import os


def save_teeth():
    root_path = 'E:\\tmp_data\\1'
    case = Case.objects.get(pk=1)
    patient = case.patient
    for i in range(1, 5):
        for j in range(1, 8):
            tooth_path = os.path.join(root_path, str(i) + str(j) + '.stl')
            if not os.path.exists(tooth_path):
                continue
            path = Path(tooth_path)
            file = path.open(mode='rb')
            d_file = File(file, name=path.name)
            tooth = ToothFile(patient=patient, case=case, quadrant_type=i, position_type=j, file=d_file)
            tooth.save()
