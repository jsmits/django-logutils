from django.http import HttpResponse


def empty_view(request, *args, **kwargs):
    return HttpResponse('')

def non_empty_view(request, *args, **kwargs):
    return HttpResponse('dummy')

