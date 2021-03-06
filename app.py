from flask import Flask,request
import json
import requests
from langdetect import detect

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
    try:
        jsonData = request.get_json()
        entry = jsonData['entry']
        messaging = entry[0]["messaging"]
        for item in messaging :
            if "message" in item and "text" in item["message"]:
                #extract sender from messaging
                recipient = item["recipient"]
                sender = item["sender"]

                #extract incoming message from messaging
                msg = item["message"]
#                encodeMsg = msg["text"].encode("utf-8")
                responseMsg = WordResponse(msg["text"])

                #echo back to sender
                echo_to_sender(recipient["id"], sender["id"], responseMsg)

        return json.dumps({'success':True}),200,{'Content-Type':'application/json'}
    except:
        return "Failed"

def echo_to_sender(recipient_id, sender_id, msg_txt):
    print("recipient ", recipient_id)
    print("sender ", sender_id)
    print("msg_txt ", msg_txt.encode("utf-8"))
    req = requests.post(
         "https://graph.facebook.com/v2.6/me/messages",
         params = {"access_token":access_token},
         data = json.dumps({
            "recipient":{"id":sender_id},
            "message": {"text":msg_txt}
          }),
         headers = {'Content-Type':'application/json; charset=utf-8'})
    print("Message was sent")

def WordResponse(message):
    print("response for ", message.encode("utf-8"))
    responseText = "ฉันไม่เข้าใจประโยคนี้"
    
    lang = detect(message)
    print ("DETECTED LANGUAGE", lang.strip())
    if (not IsContain("th", lang)):
        message = message.lower()
        words = message.split(" ")
        
        if "hi" in words:
            responseText = "Sawasdee Ka"
        elif "hello" in words:
            responseText = "Sawasdee Ka"
        elif "sawasdee" in words:
            responseText = "Sawasdee Ka"
        else:
            responseText = "Sorry. Could you speak Thai?"
    else:
        print ("THAI")
        if IsContain("สวัสดี", message):
            responseText = "สวัสดีค่ะ"
        elif IsContain("ดีจ้า", message):
            responseText = "ดีจร้า"
        elif IsContain("ทำไร", message):
            responseText = "ตอบแช็ทอยู่ค่ะ"
        elif IsContain("ทำอะไร", message):
            responseText = "ตอบแช็ทอยู่ค่ะ"
        elif IsContain("ชื่ออะไร", message):
            responseText = "ตอนนี้โปรแกรมเมอร์ยังไม่ได้ตั้งชื่อให้ค่ะ"
        elif IsContain("อยากรู้จัก", message):
            responseText = "ยินดีได้รู้จักค่ะ"
        elif IsContain("อยู่ไหน", message):
            responseText = "ม.กรุงเทพค่ะ"
        elif IsContain("อยู่ที่ไหน", message):
            responseText = "ม.กรุงเทพค่ะ"
        elif IsContain("โปรแกรมเมอร์หน้าตาดี", message):
            responseText = "ใช่ค่ะ โปรแกรมเมอร์ของเราหน้าตาดีมากกกก\nก.ไก่ล้านตัว"
        elif IsContain("สุดๆ", message):
            responseText = "สุดๆ ไปเลยค่าาาา"
        elif IsContain("ไปหา", message):
            responseText = "มาเรียนม.กรุงเทพสิคะ"
        elif IsContain("กวน", message):
            responseText = "ไม่ได้กวนนะคะ"
   
    return responseText

def IsContain(word, message):
    if word.encode("utf-8") in message.encode("utf-8"):
        return True
    else:
        return False

