from django.shortcuts import render
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from .config import username, apikey, username1, apikey1
from django.views.decorators.csrf import csrf_exempt
from .models import User, Product, session_levels
import datetime
from django.http import HttpResponse
from .methods import requested_location, requested_price, requested_town, final_list, details_generator, get_phonenumbers

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
            response = "CON Which is your county? e.g.\n  Nairobi\n Uasin Gishu\n Machakos\ne.t.c ..."
            return HttpResponse(response, content_type='text/plain')
        if level == 2:
            session_level3 = User.objects.get(phonenumber = phoneNumber)
            session_level3.level=3
            session_level3.location = userResponse
            session_level3.save()
            response = "CON What is your closest town or market center?.\n e.g. Makutano"
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
            response = "CON Enter the quantity (units: Kgs, Bags, Litres, Trays, e.t.c.)\n e.g 1, 10, 100"
            return HttpResponse(response, content_type='text/plain')

        if level == 5:
            session_level6 = User.objects.get(phonenumber = phoneNumber)
            session_level6.level=6
            response = "CON Enter the price per Kg\n. e.g. 50, 100, 1000"
            return HttpResponse(response, content_type='text/plain')

        if level == 6:
            session_level7 = User.objects.get(phonenumber = phoneNumber)
            session_level7.level=7
            product = Product.objects.create(type_of_product=textList[0],name=textList[4], quantity=textList[5], price=textList[6], user=user)
            product.save()
            response = "END Your request has been received. \n We will send you a message with contact details of a buyer/seller that matches your request."
            # this are variables to be used by the generate details section
            current_product = textList[4].lower()
            current_price = textList[6]
            current_town = textList[3].lower()
            current_location = textList[2].lower()
            current_phonenumber = phoneNumber
            current_type = textList[0]

            # this is the message generator section that determines the message that will be sent to the current user
            requested_products = Product.requested_products(current_product)


            # this is a list of products which satisfy the price requirements of the user
            list_price = requested_price(current_price, current_type, requested_products)

            # this is a list of products that satisfy the location requirements of the current user
            list_town = requested_town(current_town, list_price)

            # this is a list of products that satisfy the current user's location requirements

            list_location = requested_location(current_location, list_price)

            # this is the final list that always returns atleast three products based on availability of those products

            results_list = final_list(requested_products, list_price, list_location, list_town)

            # this is a list of phonenumbers that the current users will get

            found_phonenumbers = get_phonenumbers(results_list)

            # these are message details to be sent to the farmer

            contacts = details_generator(found_phonenumbers)
            print(contacts)

            username = username1
            apiKey = apikey1

            to = phoneNumber
            message = 'Thank you '+ user.name + ' for using our services.\n' \
                      'This is your entry:\n\n' \
                      'Product Name: '+ textList[4] + '\n' \
                      'Quantity: '+ textList[5] + '\n' \
                      'Price: ' + textList[6] + '\n\n' \
                      'If this entry is accurate, we will send you information matching your request.\n' \
                                                'If you would like to make another entry dial. \n*384*10446#'
            message1 = 'Find below contact the numbers below matching your request: \n' + contacts


            gateway = AfricasTalkingGateway(username, apiKey)

            try:
                # That's it, hit send and we'll take care of the rest.

                results = gateway.sendMessage(to, message)
                results1 = gateway.sendMessage(to, message1)

                for recipient in results:
                    # status is either "Success" or "error message"
                    print('number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
                                                                        recipient['status'],
                                                                        recipient['messageId'],
                                                                        recipient['cost']))

                for recipient in results1:
                    # status is either "Success" or "error message"
                    print('number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
                                                                        recipient['status'],
                                                                        recipient['messageId'],
                                                                        recipient['cost']))

            except AfricasTalkingGatewayException as e:
                print('Encountered an error while sending: %s' % str(e))


            return HttpResponse(response, content_type='text/plain')



def index(request):

    return render(request, 'index.html')
