import websocket
import _thread
import time
import rel
from os import system
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from time import sleep
def date():
    return (datetime.now()).strftime("%m/%d/%Y %H:%M:%S")
def savedata(id,x):
    global db
   
    data = x

    doc_ref = db.collection('MATIC').document(str(id))
    doc_ref.set(x)
    print("id {} x {}".format(id,x))
def on_message(ws, message):
    sleep(30)
    x=eval(message)
    remaining=x['events'][0]["remaining"]
    eventId=x['eventId']
    types=x['events'][0]['type']
    
    savedata(eventId,{
        "date":date(),
        "price":x['events'][0]['price'],
        "remaining":remaining
    })
    print(f"id :{eventId} price :{x['events'][0]['price']} remaining : {remaining}")
    exit
    pass
def on_error(ws, error):
    #print(error)
    pass
def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
def lt():
    #websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://api.gemini.com/v1/marketdata/MATICUSD",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    system("cls")
    print("hi")
    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()

if __name__ == "__main__":
    
    # Initialize Firebase with your credentials
    cred = credentials.Certificate('m.json')
    firebase_admin.initialize_app(cred)

    # Get a reference to the Firestore database
    db = firestore.client()
    lt()
    print("hi")
    
