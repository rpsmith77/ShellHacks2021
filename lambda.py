import json
import random
import decimal
import os
import logging
import traceback

debug=True


# on error, return nice message to bot
def fail(intent_request,error):
    #don't share the full eerror in production code, it's not good to give full traceback data to users
    error = error if debug else ''
    intent_name = intent_request['sessionState']['intent']['name']
    message = {
                'contentType': 'PlainText',
                'content': f"Oops... I guess I ran into an error I wasn't expecting... Sorry about that. My dev should probably look in the logs.\n {error}"
                }
    fulfillment_state = "Fulfilled"
    return close(intent_request, get_session_attributes(intent_request), fulfillment_state, message) 
       
#mock data query against inventory.json instead of a database or using an api call
def query_data(make,vehicle_type):
    inventory_path = os.environ['LAMBDA_TASK_ROOT'] + "/inventory.json"
    content=open(inventory_path).read()
    inventory_json=json.loads(content)
    filtered= [v for v in inventory_json if make==v['make'] and vehicle_type==v['type']]
    return filtered

'''''
=== UTIL METHODS ===========================
'''''

#util method to get the slots fromt he request
def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']

#util method to get a slot's value
def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None and 'interpretedValue' in slots[slotName]['value']:
        return slots[slotName]['value']['interpretedValue']
    else:
        return None
#gets a map of the session attributes
def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']

    return {}
# builds response to tell the bot you want to trigger another intent (use to switch the context)
def elicit_intent(intent_request, session_attributes, message):
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            },
            'sessionAttributes': session_attributes
        },
        'messages': [ message ] if message != None else None,
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }
# builds response to tell the bot you need to get the value of a particular slot
def elicit_slot(intent_request, session_attributes,slot_to_elicit, message):
    intent_request['sessionState']['intent']['state'] = 'InProgress'
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': slot_to_elicit
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }
# builds response to end the dialog
def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }



'''
==== intent handlers =====
'''


# --------------------------------------- Jairo Code Stuff ---------------------------------------

# Get Website Url's
def find_Website(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    
    whatWebsite = get_slot(intent_request,'WhatWebsite')
    if whatWebsite == "main" or whatWebsite == "business":
        message = {'contentType': 'PlainText','content': 'The url for the main website is: https://www.autonationchryslerdodgejeeprambellevue.com/'}
        fulfillment_state = "Fulfilled"
        return close(intent_request, session_attributes, fulfillment_state, message)
    else:
        message = {'contentType': 'PlainText','content': 'The url for the service website is: https://www.autonation.com/schedule-store-appointment/chrysler-dodge-jeep-ram-bellevue-wa?sc_lang=en'}
        fulfillment_state = "Fulfilled"
        return close(intent_request, session_attributes, fulfillment_state, message)
        
# Get number intent
def find_phone_fax_store_or_service_number(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    which_number = get_slot(intent_request,'Location')
    if which_number == "phone":
        message = {'contentType': 'PlainText','content': '8675309'}
        fulfillment_state = "Fulfilled"
        return close(intent_request, session_attributes, fulfillment_state, message)
    if which_number == "fax":
        message = {'contentType': 'PlainText','content': 'Who uses a fax machine in the year of our lord 2021'}
        fulfillment_state = "Fulfilled"
        return close(intent_request, session_attributes, fulfillment_state, message)
    if which_number == "storeID":
        message = {'contentType': 'PlainText','content': 'Store #1337'}
        fulfillment_state = "Fulfilled"
        return close(intent_request, session_attributes, fulfillment_state, message)
    if which_number == "service":
        message = {'contentType': 'PlainText','content': 'Service #42'}
        fulfillment_state = "Fulfilled"
        return close(intent_request, session_attributes, fulfillment_state, message)
    else:
        message = {'contentType': 'PlainText','content': 'The value could not be understood, please try again.'}
        fulfillment_state = "Fulfilled"
        return close(intent_request, session_attributes, fulfillment_state, message)
        
# Get Store Hours
def get_store_hours(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    
    store_section = get_slot(intent_request,'Section')
    day_of_week = get_slot(intent_request, 'Day')
    
    if store_section == "sales":
        if day_of_week.lower() == "monday" or day_of_week.lower() == "tuesday" or day_of_week.lower() == "wednesday" or day_of_week.lower() == "thursday" or day_of_week.lower() == "friday":
            message = {'contentType': 'PlainText','content': 'On {day}, sales opens at 7:00 AM and closes at 7:00PM'.format(day = day_of_week)}
            fulfillment_state = "Fulfilled"
            return close(intent_request, session_attributes, fulfillment_state, message)
        
        if day_of_week.lower() == "saturday":
            message = {'contentType': 'PlainText','content': 'On Saturday, sales opens at 8:00 AM and closes at 5:00PM'}
            fulfillment_state = "Fulfilled"
            return close(intent_request, session_attributes, fulfillment_state, message)
        
        if day_of_week.lower() == "sunday":
            message = {'contentType': 'PlainText','content': 'The store is closed on Sunday'}
            fulfillment_state = "Fulfilled"
            return close(intent_request, session_attributes, fulfillment_state, message)
            
    elif store_section == "service":
        if day_of_week.lower() == "monday" or day_of_week.lower() == "tuesday" or day_of_week.lower() == "wednesday" or day_of_week.lower() == "thursday" or day_of_week.lower() == "friday":
            message = {'contentType': 'PlainText','content': 'On {day}, service opens at 7:00 AM and closes at 7:00PM'.format(day = day_of_week)}
            fulfillment_state = "Fulfilled"
            return close(intent_request, session_attributes, fulfillment_state, message)
        
        if day_of_week.lower() == "saturday":
            message = {'contentType': 'PlainText','content': 'On Saturday, service opens at 8:00 AM and closes at 5:00PM'}
            fulfillment_state = "Fulfilled"
            return close(intent_request, session_attributes, fulfillment_state, message)
        if day_of_week.lower() == "Sunday":
            message = {'contentType': 'PlainText','content': 'The store is closed on Sunday'}
            fulfillment_state = "Fulfilled"
            return close(intent_request, session_attributes, fulfillment_state, message)
            
    elif store_section == "collision":
        if day_of_week.lower() == "monday" or day_of_week.lower() == "tuesday" or day_of_week.lower() == "wednesday" or day_of_week.lower() == "thursday" or day_of_week.lower() == "friday":
            message = {'contentType': 'PlainText','content': 'On {day}, collision opens at 8:00 AM and closes at 6:00PM'.format(day = day_of_week)}
            fulfillment_state = "Fulfilled"
            return close(intent_request, session_attributes, fulfillment_state, message)
            
        if day_of_week.lower() == "saturday":
            message = {'contentType': 'PlainText','content': 'On Saturday, collision opens at 8:00 AM and closes at 6:00PM'}
            fulfillment_state = "Fulfilled"
            return close(intent_request, session_attributes, fulfillment_state, message)
            
        if day_of_week.lower() == "sunday":
            message = {'contentType': 'PlainText','content': 'The store is closed on Sunday'}
            fulfillment_state = "Fulfilled"
            return close(intent_request, session_attributes, fulfillment_state, message)
            
    #elif store_section == "service":
    else:
        message = {'contentType': 'PlainText','content': 'The value could not be understood, please try one from this list: sales, .'}
        fulfillment_state = "Fulfilled"
        return close(intent_request, session_attributes, fulfillment_state, message)
        
            

#handler for when there is no matching intent handler
def default_response(intent_request):
    session_attributes = get_session_attributes(intent_request)
    intent_name = intent_request['sessionState']['intent']['name']
    message = {
        'contentType': 'PlainText',
        'content': f"This lambda doesn't know how to process intent_name={intent_name}"
    }
    fulfillment_state = "Fulfilled"
    return close(intent_request, session_attributes, fulfillment_state, message)
    

#looks at the intent_name and routes to the handler method    
def dispatch(intent_request):
    try:
        intent_name = intent_request['sessionState']['intent']['name']
        response = None
        # Dispatch to your bot's intent handlers
        if intent_name == 'AskForWebsite':
            return find_Website(intent_request)
        elif intent_name == 'GetNumber':
            return find_phone_fax_store_or_service_number(intent_request)
        elif intent_name == 'GetStoreHours':
            return get_store_hours(intent_request)
        else:
            return default_response(intent_request)
    except Exception as ex:
        error = traceback.format_exc()
        print(error)
        return fail(intent_request,error)


    
#entry point of lambda
def lambda_handler(event, context):
    print(json.dumps(event))
    response = dispatch(event)
    return response
