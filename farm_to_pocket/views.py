from django.shortcuts import render
from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)
from .config import username, apikey
from django.views.decorators.csrf import csrf_exempt
from .models import User, session_levels
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
            level = 0

        # Serve basic menu
        if level == 0 or level == 1:
            if userResponse == '';
                if level == 0:
                    session_level1 = User.objects.get(phonenumber=phoneNumber)
                    session_level1.level = 1
                    session_level1.save()

                    response = 'Welcome to FarmToPocket. would you like to buy or sell?'
                    response += '1. Buyer.\n'
                    response += '2. Seller.\n'

                    return HttpResponse(response, content_type='text/plain')
            if userResponse == '1':
                if level == 1:
                    response = 'What would you like to sell?'
                    response +=  '1. Beans.\n'
                    response +=  '2. Maize.\n'
                    response +=  '3. Wheat.\n'
                    response +=  '4. Milk.\n'
                    response +=  '5. Sukuma Wiki.\n'
                    response +=  '6. Cabbage.\n'
                    response +=  '7. Managu.\n'
