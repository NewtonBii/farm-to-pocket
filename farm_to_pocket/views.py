from django.shortcuts import render
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from .config import username, apikey
from django.views.decorators.csrf import csrf_exempt
from .models import User, session_levels
import datetime
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

        if level == 0:
            if userResponse == "":
                session_level1 = User.objects.get(phonenumber=phoneNumber)
                session_level1.level=1
                session_level1.save()

                response = "CON Welcome to FarmerService. Are you buying or selling?"
                response += "1. Buyer. \n"
                response += "2. Seller. \n"

                return HttpResponse(response, content_type='text/plain')
                
