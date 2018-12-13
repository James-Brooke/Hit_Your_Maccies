from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("If it fits your maccies to go here.")

    