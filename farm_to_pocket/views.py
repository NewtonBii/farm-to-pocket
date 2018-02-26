from django.shortcuts import render
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from .config import username, apikey
from django.views.decorators.csrf import csrf_exempt
from .models import Buyer, Seller, Product, session_levels
import datetime
from django.http import HttpResponse

# Create your views here.
@csrf_exempt
def callback(request):
    """Function that handles callback from Afric Stalking API"""

    if request.method == 'POST' and request.POST:
        sessionId = request.POST.get('sessionId')
        serviceCode=request.POST.get('serviceCode')
        phoneNumber=request.POST.get('phoneNumber')
        text=request.POST.get('text')
        now = datetime.datetime.now()

        textList = text.split('*')
        userResponse = textList[-1].strip()

        level = len(textList)-1

        try:
            buyer, create = Buyer.objects.get_or_create(phonenumber=phoneNumber)
            seller, create = Seller.objects.get_or_create(phonenumber=phoneNumber)
        except Buyer.DoesNotExist and Seller.DoesNotExist as e:
            level = 0
        if level == 0:
            if userResponse == "":
                response = "CON Welcome to our Service. Are you a buyer or a seller?\n"
                response += "1. Buyer\n"
                response += "2. Seller\n"

                return HttpResponse(response, content_type='text/plain')
            if userResponse == "1":
                level=1
                response = "CON Enter your name:\n"


                return HttpResponse(response, content_type='text/plain')

        if level == 1:
            print(userResponse)
            print(phoneNumber)
            response = "END Thank you."

        if userResponse == "2":
            response = "CON Enter your name:\n"
    return HttpResponse(response)
