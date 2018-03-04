
def requested_price(price,user_type,list_products):
    if user_type == 1:
        requested_type = 2
    else:
        requested_type = 1
    list_price = [] # list of produce that match the current user's price requirements
    if requested_type == 2:
        for product in list_products:
            if product.price <= price:
                list_price.append(product)
    elif requested_type == 1:
        for product in list_products:
            if product.price >= price:
                list_price.append(product)

    # you can add an else method here later to handle exceptions
    return list_price



            