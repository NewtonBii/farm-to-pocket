from django.shortcuts import render
from .AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from .config import username, apikey
from django.views.decorators.csrf import csrf_exempt
from .models import User, session_levels
# Create your views here.
# @csrf_exempt
def callback(request):
    if request.method == 'POST' and request.POST:
        sessionID = request.POST.get('sessionID')
        serviceCode = request.POST.get('serviceCode')
        phoneNumber = request.POST.get('phoneNumber')
        text = request.POST.get('text')
        now = datetime.datetime.now()

        textList = text.split('*')
        userResponse = textList[-1].strip()

        #Check level of user and if user exists
        try:
            user = User.objects.get(phonenumber=phoneNumber)
        except User.DoesNotExist as e:
            level = 0

        try:
            result, created = User.objects.get_or_create(phonenumber=phoneNumber)
        if created:
            result.save()
        if userResponse == '':
            response = 'CON Welcome to FarmToPocket Service. Would you like to buy or sell?'
            response += '1. Buyer'
            response += '2. Seller'
            if userResponse == '1':
                response = 'Please enter your full name'
