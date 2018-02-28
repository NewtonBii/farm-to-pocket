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
                response = "CON Welcome to our Service. Are you a Buyer or a seller?\n"
                response += "1. Buyer\n"
                response += "2. Seller\n"

                return HttpResponse(response, content_type='text/plain')

            session_level1 = User.objects.get(phonenumber = phoneNumber)
            session_level1.level=1
            session_level1.type_of_user = userResponse
            session_level1.save()
            response = "CON Enter your name:\n"

            return HttpResponse(response, content_type='text/plain')

        if level == 1:
            session_level2 = User.objects.get(phonenumber = phoneNumber)
            session_level2.level=2
            session_level2.name = userResponse
            session_level2.save()
            response = "CON Enter your County e.g. Nairobi, Uasin Gishu.\n"
            return HttpResponse(response, content_type='text/plain')
        if level == 2:
            session_level3 = User.objects.get(phonenumber = phoneNumber)
            session_level3.level=3
            session_level3.location = userResponse
            session_level3.save()
            response = "CON Enter your closest town center.\n"
            return HttpResponse(response, content_type='text/plain')

        if level == 3:
            session_level4 = User.objects.get(phonenumber = phoneNumber)
            session_level4.level=4
            session_level4.nearest_town = userResponse
            session_level4.save()
            response = "CON What would you like to buy?\n"
            return HttpResponse(response, content_type='text/plain')

        if level == 4:
            session_level5 = User.objects.get(phonenumber = phoneNumber)
            # product = Product.objects.create(user=user)
            session_level5.level=5
            response = "CON What quantity would you like?\n"
            return HttpResponse(response, content_type='text/plain')

        if level == 5:
            session_level6 = User.objects.get(phonenumber = phoneNumber)
            # product = Product.objects.create(user=user)
            session_level6.level=6
            response = "CON How much are you willing to pay?\n. e.g. 100 per Kg "
            return HttpResponse(response, content_type='text/plain')

        if level == 6:
            session_level7 = User.objects.get(phonenumber = phoneNumber)
            # product = Product.objects.create(user=user)
            session_level7.level=7
            response = "CON When would you like to have your product? e.g. 1 day, 1 week, 1 month...\n"
            return HttpResponse(response, content_type='text/plain')

        if level == 7:
            session_level8 = User.objects.get(phonenumber = phoneNumber)
            # product = Product.objects.create(user=user)
            session_level8.level=8
            response = "END Thank you for using the service. Your response has been recorded.\n"
            product = Product.objects.create(name = textList[4], quantity = textList[5], price=textList[6], user=user, availability = textList[7])
            product.save()
            print(textList[4])
            return HttpResponse(response, content_type='text/plain')

    return HttpResponse(response)

def index(request):
    Users = User.objects.all()

    return render(request, 'index.html', {'Users':Users})
