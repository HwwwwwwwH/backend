import os
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404, FileResponse, JsonResponse
from main.models import JawFile, ToothFile, Case
from backend.settings import MEDIA_ROOT


# Create your views here.
def index(request: HttpRequest):
    return HttpResponse('Test.')


def get_jaw_model(request: HttpRequest):
    case_id = request.GET.get('case_id')
    case = Case.objects.get(pk=case_id)
    process_type = 'Before_Segmentation'
    if request.GET.get('process_type'):
        process_type = request.GET.get('process_type')
    if not request.GET.get('position_type'):
        raise Http404('Please choose one position type [Maxillar or Mandibular]')
    else:
        position_type = request.GET.get('position_type')
    # print('case: ', case)
    # print('process_type: ', process_type)
    # print('position_type: ', position_type)
    try:
        jaw_model = JawFile.objects.get(case=case, process_type=process_type, position_type=position_type)
        file_path = os.path.join(MEDIA_ROOT, jaw_model.file.path)
        return FileResponse(open(file_path, 'rb'))
    except:
        raise Http404('No exact jaw model [case={0}}, process_type={1}, position_type={2}]'.format(case_id, process_type, position_type))


def get_teeth_list(request: HttpRequest):
    case_id = request.GET.get('case_id')
    case = Case.objects.get(pk=case_id)
    teeth_list = [False for x in range(0, 32)]
    extracted = False
    if request.GET.get('extracted'):
        extracted = request.GET.get('extracted')
    for i in range(0, 4):
        for j in range(0, 8):
            list_id = i * 8 + j
            if len(ToothFile.objects.filter(case=case, quadrant_type=i+1, position_type=j+1, isExtracted=extracted)):
                teeth_list[list_id] = True
    return JsonResponse({'teeth_list': teeth_list})


def get_tooth_model(request: HttpRequest):
    case_id = request.GET.get('case_id')
    case = Case.objects.get(pk=case_id)
    if request.GET.get('quadrant_type') and request.GET.get('position_type'):
        quadrant_type = request.GET.get('quadrant_type')
        position_type = request.GET.get('position_type')
    elif request.GET.get('teeth_id'):
        teeth_id = request.GET.get('teeth_id')
        quadrant_type = teeth_id // 8 + 1
        position_type = teeth_id % 8 + 1
    else:
        raise Http404('No quadrant or position specified.')
    try:
        tooth = ToothFile.objects.get(case=case, quadrant_type=quadrant_type, position_type=position_type)
        file_path = os.path.join(MEDIA_ROOT, tooth.file.path)
        return FileResponse(open(file_path, 'rb'))
    except:
        raise Http404('No exact tooth model [case={0}, quadrant_type={1}, position_type={2}]'
                      .format(case_id, quadrant_type, position_type))


def upload_jaw_model(request: HttpRequest):
    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        try:
            case = Case.objects.get(pk=case_id)
            patient = case.patient
        except:
            raise Http404('Can\'t find case [case_id = {}]'.format(case_id))
        for filename in request.FILES:
            if filename == 'Maxillar' or filename == 'Mandibular':
                if len(JawFile.objects.filter(pk=case_id, position_type=filename)):
                    jaw = JawFile.objects.get(pk=case_id, position_type=filename)
                else:
                    jaw = JawFile(patient=patient,
                                  case=case,
                                  process_type='Before_Segmentation',
                                  position_type=filename,
                                  file=request.FILES[filename])
                jaw.save()
        response = HttpResponse('Success')
        return response
    else:
        raise Http404('This api can be used for post only.')
