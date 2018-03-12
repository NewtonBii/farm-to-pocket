def requested_price(price, user_type, list_products):
    '''
    Method that filters based on the price requirements of the current user
    '''
    if user_type == '1':
        requested_type = '2'
    else:
        requested_type = '1'
    list_price = []  # list of produce that match the current user's price requirements
    if requested_type == '2':
        for product in list_products:
            if product.price <= int(price):
                list_price.append(product)
    elif requested_type == '1':
        for product in list_products:
            if product.price >= int(price):
                list_price.append(product)

    # you can add an else method here later to handle exceptions
    return list_price


def requested_location(location, list_price):
    '''
    Method that filters based on the location of the current user and returns a list of users matching that creteria
    '''
    list_location = []
    for product in list_price:
        if product.user.location == location:
            list_location.append(product)
    return list_location


def requested_town(town, list_price):
    '''
    Method that filters based on the nearest town of the current user and returns a list of users matching that creteria
    '''
    list_town = []
    for product in list_price:
        if product.user.nearest_town == town:
            list_town.append(product)
    return list_town


def final_list(filtered_products, list_price, list_location, list_town):
    '''
    Method that add all the list and truncates the products based on priority in terms of price,town
    and location  in that order
    '''
    final_list = list_town
    if len(final_list) < 5:
        final_list += [product for product in list_location if product not in list_town]
        if len(final_list) < 5:
            final_list += [product for product in list_price if product not in final_list]
            if len(final_list) < 5:
                final_list += [product for product in filtered_products if product not in final_list]

    return final_list


def get_phonenumbers(final_list):
    '''
    Method that takes in a list of objects and returns the phonenumbers of the
    users associated with those products as a string
    '''
    phonenumbers = {product.user.name: str(product.user.phonenumber) + '\n' +
                                       str(product.user.nearest_town) + '\n' + str(product.user.location) + "\n" + str(product.name)+ '@' +
                                       str(product.price) + '\n' for product in final_list}
    return phonenumbers


def details_generator(found_phonenumbers):
    '''
    Methods that takes in a dictionary of number and user_name and return numbers and user names as a string
    '''
    string = ''
    for item in found_phonenumbers:
        string += item + ' '
        string += found_phonenumbers[item] + '\n' + ' '

    for item in found_phonenumbers:
        details = []

    return string
