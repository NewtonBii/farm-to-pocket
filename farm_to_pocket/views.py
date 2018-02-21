from django.shortcuts import render
from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)
from .config import username, apikey
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def callback(request):
    if request.method == 'POST' and request.POST:
        sessionID = request.POST.get('sessionID')
        serviceCode = request.POST.get('serviceCode')
        phoneNumber = request.POST.get('phoneNumber')
        text = request.POST.get('text')
        now = datetime.datetime.now()

        textList = text.split('*')
        userResponse = textList[-1].strip()

        try:
            session = User.objects.get(phonenumber=phoneNumber)
            level = session.level
        except User.DoesNotExist as e:
            
