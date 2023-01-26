from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404
from main.models import JawFile, Case


# Create your views here.
def index(request: HttpRequest):
    return HttpResponse('Test.')


def get_jaw_model(request: HttpRequest):
    case_id = request.GET.get('case_id')
    case = Case.objects.get(pk=case_id)
    print(case.case_id)
    jaw_models = JawFile.objects.filter(case=case)
    if len(jaw_models) != 2:
        return Http404('The number of jaw model is not 2.')
    return HttpResponse('Jaw Model')
