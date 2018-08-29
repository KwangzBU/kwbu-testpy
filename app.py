from flask import Flask,request
import json
import requests

app = Flask(__name__)

#copy from Facebook
access_token = 'EAADbooHcUsgBAP8otjQa8wyt0ok0uMsRFTroIyifiUtNZASN3frkIPWhqhpzdPmv0d6L4vQSAQYZBADSJSvXDsoJyMGcD4OmK5swcROaEeYpsjWwekNwU0l0pCrKhqKjldfk8gwBDZBWZBv0ZAENRUgRaWklBzoT9k5V0Vi6LFwZDZD'

@app.route('/test',methods=['GET'])
def do_test():
     return "Hello"

@app.route('/',methods=['GET'])
def verification_handle():
    verify_token = request.args.get('hub.verify_token','')
    print(verify_token)
    challenge = request.args.get('hub.challenge', '') 
    if verify_token == "bubotisthebest":
        return challenge
    else:
        return "Wrong validation"

    
@app.route('/',methods=['POST'])
def incoming_message_handle():
    #get data from request
    payload = request.get_data()
    print("payload ", payload)

    #turn payload to json
    json_data = json.loads(payload)

    #extract entry, entry is an array
    entry = json_data['entry']
    print("entry ", entry)

    #extract messaging from entry, messaging is an array
    messaging = entry[0]["messaging"]
    print("messaging", messaging)

    for item in messaging :
        print ("item ", item)
        if "message" in item and "text" in item["message"] :
            #extract sender from messaging
            sender = item["sender"]
            print("sender ", sender)

            #extract incoming message from messaging
            msg = item["message"]
            print("msg ", msg)

            #echo back to sender
            echo_to_sender(sender["id"],msg["text"].encode('unicode_escape'))

    #tell Facebook that every is alright
    return json.dumps({'success':True}),200,{'Content-Type':'application/json'}


def echo_to_sender(sender_id,msg_txt):
    # get this from Facebook manual
    req = requests.post(
         "https://graph.facebook.com/v2.6/me/messages",
         params = {"access_token":access_token},
         data = json.dumps({
            "recipient":sender_id,
            "message": msg_txt
          }),
         headers = {'Content-Type':'application/json'})
    
'''
@app.route('/',methods=['POST'])
def incoming_message_handle():
    #get data from request
    payload = request.get_data()
    
    #turn payload to json
    json_data = json.loads(payload)

    #extract entry, entry is an array
    entry = json_data['entry']

    #extract messaging from entry, messaging is an array
    messaging = entry[0]["messaging"]

    for item in messaging :
      if "message" in item and "text" in item["message"] :

        #extract sender from messaging
        sender = item["sender"]

        #extract incoming message from messaging
        msg = item["message"]

        #echo back to sender
        echo_to_sender(sender["id"],msg["text"].encode('unicode_escape'))

    #tell Facebook that every is alright
    return json.dumps({'success':True}),200,{'Content-Type':'application/json'}


def echo_to_sender(sender_id,msg_txt):
    # get this from Facebook manual
    req = requests.post(
         "https://graph.facebook.com/v2.6/me/messages",
         params = {"access_token":access_token},
         data = json.dumps({
            "recipient":sender_id,
            "message": msg_txt
          }),
         headers = {'Content-Type':'application/json'})
'''