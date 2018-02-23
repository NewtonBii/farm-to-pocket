from django.shortcuts import render
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from .config import username, apikey
from django.views.decorators.csrf import csrf_exempt
from .models import User, session_levels
import datetime
from django.http import HttpResponse
# Create your views here.
@csrf_exempt
def callback(request):

    if request.method == 'POST' and request.POST:
        sessionId = request.POST.get('sessionId')
        serviceCode=request.POST.get('serviceCode')
        phoneNumber=request.POST.get('phoneNumber')
        text=request.POST.get('text')
        now = datetime.datetime.now()

        textList = text.split('*')
        userResponse = textList[-1].strip()

        result, created = User.objects.get_or_create(phonenumber=phoneNumber)

        if userResponse == "":
            response = "CON Welcome to our Service. Are you a buyer or a seller?\n"
            response += "1. Buyer\n"
            response += "2. Seller\n"
            return HttpResponse(response, content_type='text/plain')
        if userResponse == "1":
            if created:
                result.save()
                response = "CON Enter your name:\n"
                return HttpResponse(response, content_type='text/plain')
            # if not created:
            #     if not result.name:
            #         result.name = userResponse
            #         result.save()
            #
            #         response = "CON Enter your location"
            #         return render(response, content_type='text/plain')
            #     if not result.location:
            #         result.location = userResponse
            #         result.save()
    return render(request, 'index.html')
