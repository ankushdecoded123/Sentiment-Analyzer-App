from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.conf import settings
from django.http import Http404

from .apps import TweetanalysisappConfig

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

# Create your views here.

class call_model(APIView):
    def get(self, request):
        if request.method == 'GET':

            text = request.GET.get('text')
            tw = TweetanalysisappConfig.tokenizer.texts_to_sequences([text])
            tw = TweetanalysisappConfig.pad_sequences(tw,maxlen=200)
            prediction = int(TweetanalysisappConfig.my_model.predict(tw).round().item())

            if prediction == 0:
                response = {'sentiment': 'positive'}
            else:
                response = {'sentiment': 'negative'}

            return JsonResponse(response)
        else:
            return JsonResponse(status.HTTP_400_BAD_REQUEST)

def home(request):
    val=''
    if request.method == 'POST':
        val = request.POST.get('next')
        print(val)

    template = "index.html"
    context = {'data' : analyze_data(val)}
    return render(request, template, context)

def analyze_data(text):
    if not text:
        return 'Waiting for a text to analyze.'

    tw = TweetanalysisappConfig.tokenizer.texts_to_sequences([text])
    tw = TweetanalysisappConfig.pad_sequences(tw,maxlen=200)
    prediction = int(TweetanalysisappConfig.my_model.predict(tw).round().item())

    if prediction == 0:
        return 'Seems like its POSITIVE... :)'
    else:
        return 'Awww, so sad! its NEGATIVE'


