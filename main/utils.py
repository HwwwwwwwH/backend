from main.models import ToothPosition
from pyquaternion import Quaternion


def toothPosition2Quaternion(tooth_position: ToothPosition):
    return Quaternion(axis=[tooth_position.x, tooth_position.y, tooth_position.z], angle=tooth_position.angle)
