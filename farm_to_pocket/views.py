from django.shortcuts import render
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from .config import username, apikey
from django.views.decorators.csrf import csrf_exempt
from .models import User, Product, session_levels
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
            user, create = User.objects.get_or_create(phonenumber=phoneNumber)
        except User.DoesNotExist as e:
            level = 0

        if level == 0:
            if userResponse == "":
                response = "CON Welcome to onPoint Service. Would you like to buy or sell?\n"
                response += "1. I am Buying\n"
                response += "2. I am a Seller\n"

                return HttpResponse(response, content_type='text/plain')

            session_level1 = User.objects.get(phonenumber = phoneNumber)
            session_level1.level=1
            session_level1.type_of_user = userResponse
            session_level1.save()
            response = "CON Please enter your name:\n"

            return HttpResponse(response, content_type='text/plain')

        if level == 1:
            session_level2 = User.objects.get(phonenumber = phoneNumber)
            session_level2.level=2
            session_level2.name = userResponse
            session_level2.save()
            response = "CON Which is your county? \n e.g. Nairobi, Uasin Gishu, Machakos\n"
            return HttpResponse(response, content_type='text/plain')
        if level == 2:
            session_level3 = User.objects.get(phonenumber = phoneNumber)
            session_level3.level=3
            session_level3.location = userResponse
            session_level3.save()
            response = "CON What is your closest town or market center?.\n e.g. Kijabe Town or Ngong Town"
            return HttpResponse(response, content_type='text/plain')

        if level == 3:
            session_level4 = User.objects.get(phonenumber = phoneNumber)
            session_level4.level=4
            session_level4.nearest_town = userResponse
            session_level4.save()
            response = "CON Enter the product name\ne.g. Maize, Beans, Milk"
            return HttpResponse(response, content_type='text/plain')

        if level == 4:
            session_level5 = User.objects.get(phonenumber = phoneNumber)
            session_level5.level=5
            response = "CON Enter the quantity: in Kgs\n e.g 1, 10, 100"
            return HttpResponse(response, content_type='text/plain')

        if level == 5:
            session_level6 = User.objects.get(phonenumber = phoneNumber)
            session_level6.level=6
            response = "CON Enter the price per Kg\n. e.g. 50, 100, 1000"
            return HttpResponse(response, content_type='text/plain')

        if level == 6:
            session_level7 = User.objects.get(phonenumber = phoneNumber)
            session_level7.level=7
            response = "CON When is it available?\n When do you need it?\n e.g. 1 day, 1 week, 1 month...\n"
            return HttpResponse(response, content_type='text/plain')

        if level == 7:
            session_level8 = User.objects.get(phonenumber = phoneNumber)
            session_level8.level=8
            response = "END Your request has been recieved. \n We will send you a message with contact details of a buyer/seller that matches your request."
            product = Product.objects.create(name = textList[4], quantity = textList[5], price=textList[6], user=user, availability = textList[7])
            product.save()
            print(textList[4])
            return HttpResponse(response, content_type='text/plain')

    return HttpResponse(response)

def index(request):
    Users = User.objects.all()

    return render(request, 'index.html', {'Users':Users})
