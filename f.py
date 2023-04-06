import websocket
import _thread
import time
from os import system
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from time import sleep

def date():
    return (datetime.now()).strftime("%m/%d/%Y %H:%M:%S")

def savedata(id, x):
    global db
   
    data = x

    doc_ref = db.collection('MATIC').document(str(id))
    doc_ref.set(x)
    print("id {} x {}".format(id, x))

def on_message(ws, message):
    sleep(30)
    x = eval(message)
    remaining = x['events'][0]["remaining"]
    eventId = x['eventId']
    types = x['events'][0]['type']
    
    savedata(eventId, {
        "date": date(),
        "price": x['events'][0]['price'],
        "remaining": remaining
    })
    
    print(f"id :{eventId} price :{x['events'][0]['price']} remaining : {remaining}")
    exit

def on_error(ws, error):
    #print(error)
    pass

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    lt()
def on_open(ws):
    print("Opened connection")

def lt():
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://api.gemini.com/v1/marketdata/MATICUSD",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    
    system("clear")
    print("hi")
    # Set the ping interval to 5 seconds and the ping timeout to 2 seconds
    ws.run_forever(ping_interval=5, ping_timeout=2)  
    

if __name__ == "__main__":
    # Initialize Firebase with your credentials
    cred = credentials.Certificate('m.json')
    firebase_admin.initialize_app(cred)

    # Get a reference to the Firestore database
    db = firestore.client()
    lt()
    print("hi")
