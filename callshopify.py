import json
import requests
import sys
import os

def fetchdata(cust):

    #Shopify API Information
    store_name = os.environ.get('SHOPIFY_STORE')
    shopify_url = 'https://' + str(store_name)  + '.myshopify.com/admin/'
    shopify_api_key = os.environ.get('SHOPIFY_API_KEY')
    shopify_api_pass = os.environ.get('SHOPIFY_API_PASS')

    #User email to search for
    email = cust

    #Fetch Customer Data by Email and JSON It
    url = shopify_url + "customers/search.json?query=email:" + email
    r = requests.get(url, auth=(shopify_api_key, shopify_api_pass))
    c = r.json()

    #If "customers" object exists in response, search was succesful
    if c.get('customers'):
        #create customer and address objects from response data
        customer = c['customers'][0]
        address = customer['default_address']

        #Parse Key Info from Shopify Customer Response
        custId = customer['id']
        custName =  customer['first_name'] + ' ' + customer['last_name']
        lastOrderId = customer['last_order_id']

        #Fetch Last Order Data from Shopify using lastOrderId
        url = shopify_url + "orders/" + str(lastOrderId) + ".json"
        l = requests.get(url, auth=(shopify_api_key, shopify_api_pass))
        o = l.json()
        order = o['order']

        #Parse Response from Shopify of Last Order Data
        #Build List of Line Items Ordered
        line_items = ""
        for line in order['line_items']:
            sku = line['sku']

            #If Set or Kit, break out line item properties
            if sku.startswith(('SET', 'KIT')):
                line_items += '+ {}<br/>'.format(sku)
                for prop in line['properties']:
                    item_sku = prop['value']
                    line_items += '+++ {}<br/>'.format(item_sku)
            #Otherwise just include SKU
            else:
                line_items += '+ {}<br/>'.format(sku)

        #Fetch All Order Data from Shopify using custId
        url = shopify_url + "customers/" + str(custId) + "/orders.json"
        rs = requests.get(url, auth=(shopify_api_key, shopify_api_pass))
        ors = rs.json()
        allors = ors['orders']

        all_orders = ""
        for order in allors:
            id = order['id']
            all_orders += '{}, '.format(id)

        #Construct JSON Payload for Response
        payload = json.dumps({
            "custId":  custId,
            "custName": custName,
            "createdAt": customer['created_at'],
            "lastOrder": customer['last_order_name'],
            "lastOrderId": str(lastOrderId),
            "numOrders": customer['orders_count'],
            "totalSpend": customer['total_spent'],
            "phone": address['phone'],
            "address1": address['address1'],
            "address2": address['address2'],
            "city": address['city'],
            "state": address['province_code'],
            "zip": address['zip'],
            "loTotal": order['total_price'],
            "loDate": order['created_at'],
            "skus": line_items,
            "allOrders": all_orders
        })

    #If inital Shopify Result is empty, return error message
    else:
        #Construct Payload for Response
        payload = json.dumps({
            "custName":  "No Customer With This Email"
            })

    return payload
