#                                                   8 8                                                                                                            
#                                                ad88888ba     ,ad8888ba,   88888888ba   88  88888888ba  888888888888     88        88  88        88  88888888ba   
#                                               d8" 8 8 "8b   d8"'    `"8b  88      "8b  88  88      "8b      88          88        88  88        88  88      "8b  
#                                               Y8, 8 8      d8'            88      ,8P  88  88      ,8P      88          88        88  88        88  88      ,8P  
#                                               `Y8a8a8a,    88             88aaaaaa8P'  88  88aaaaaa8P'      88          88aaaaaaaa88  88        88  88aaaaaa8P'  
#                                                 `"8"8"8b,  88             88""""88'    88  88""""""'        88          88""""""""88  88        88  88""""""8b,  
#                                                   8 8 `8b  Y8,            88    `8b    ""  88               88          88        88  88        88  88      `8b  
#                                               Y8a 8 8 a8P   Y8a.    .a8P  88     `8b   aa  88               88          88        88  Y8a.    .a8P  88      a8P  
#                                                "Y88888P"     `"Y8888Y"'   88      `8b  88  88               88          88        88   `"Y8888Y"'   88888888P"   
#                                                   8 8                                                                                                            

import websocket
import json
import threading
import time

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def recieve_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    print("heartbeat begin")
    while True:
        time.sleep(interval)
        heartbeatJSON = {"op": 1, "d": "null"}
        send_json_request(ws, heartbeatJSON)
        print("heartbeat sent")

ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=6&encording=json")
event = recieve_json_response(ws)

heartbeat_intervals = event['d']['heartbeat_interval'] / 10000
print("heartbeat_intervals = ", heartbeat_intervals)
threading._start_new_thread(heartbeat, (heartbeat_intervals, ws))

token = "TOKEN"

payload = {'op': 2, "intents": 513, 'd':{"token": token, "properties": {"$os": "windows", "$browser": "chrome", "$device": "pc"}}}
send_json_request(ws, payload)

while True:
    event = recieve_json_response(ws)
    try:
        print(f"{event['d']['author']['username']}: {event['d']['content']}")
        op_code = event('op')
        if op_code == 11:
            print('hearth reivedd')
    except:
        pass
