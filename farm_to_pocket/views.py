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

        if level == 0:
            if userResponse == "":
                response = "CON Welcome to our Service. Are you a buyer or a seller?\n"
                response += "1. Buyer\n"
                response += "2. Seller\n"

                return HttpResponse(response, content_type='text/plain')
            if userResponse == "1":
                try:
                    buyer, create = Buyer.objects.get_or_create(phonenumber=phoneNumber)
                    # seller, create = Seller.objects.get_or_create(phonenumber=phoneNumber)
                except Buyer.DoesNotExist as e:
                    level = 0

                session_level1 = Buyer.objects.get(phonenumber = phoneNumber)
                session_level1.level=1
                session_level1.save()
                response = "CON Enter your name:\n"

                return HttpResponse(response, content_type='text/plain')

        if level == 1:
            session_level2 = Buyer.objects.get(phonenumber = phoneNumber)
            session_level2.level=2
            session_level2.name = userResponse
            session_level2.save()
            response = "CON Enter your County e.g. Nairobi, Uasin Gishu.\n"
            return HttpResponse(response, content_type='text/plain')
        if level == 2:
            session_level3 = Buyer.objects.get(phonenumber = phoneNumber)
            session_level3.level=3
            session_level3.location = userResponse
            session_level3.save()
            response = "CON Enter your closest town center.\n"
            return HttpResponse(response, content_type='text/plain')

        if level == 3:
            session_level4 = Buyer.objects.get(phonenumber = phoneNumber)
            session_level4.level=4
            session_level4.nearest_town = userResponse
            session_level4.save()
            response = "CON What would you like to buy?\n"
            return HttpResponse(response, content_type='text/plain')

        if level == 4:
            session_level5 = Buyer.objects.get(phonenumber = phoneNumber)
            session_level5.level=5
            session_level5.product = userResponse
            session_level5.save()
            response = "CON What quantity would you like?\n"
            return HttpResponse(response, content_type='text/plain')

        if level == 5:
            session_level6 = Buyer.objects.get(phonenumber = phoneNumber)
            session_level6.level=6
            session_level6.quantity = userResponse
            session_level6.save()
            response = "CON How much are you willing to pay?\n. e.g. 100 per Kg "
            return HttpResponse(response, content_type='text/plain')

        if level == 6:
            session_level7 = Buyer.objects.get(phonenumber = phoneNumber)
            session_level7.level=7
            session_level7.price = userResponse
            session_level7.save()
            response = "CON When would you like to have your product? e.g. 1 day, 1 week, 1 month...\n"
            return HttpResponse(response, content_type='text/plain')

        if level == 7:
            session_level8 = Buyer.objects.get(phonenumber = phoneNumber)
            session_level8.level=8
            session_level8.availability = userResponse
            session_level8.save()
            response = "END Thank you for using the service. Your response has been recorded.\n"
            return HttpResponse(response, content_type='text/plain')

        if userResponse == "2":
            try:
                seller, create = Seller.objects.get_or_create(phonenumber=phoneNumber)
            except Seller.DoesNotExist as e:
                level = 0
            response = "CON Enter your name:\n"

    return HttpResponse(response)

def index(request):
    
    return render(request, 'index.html')
