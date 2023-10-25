banner = '''
                                                                                 
                                                                       .,***,..                                      
                                                                .@@@@@@@@@@@@@@@@@@@@@@.                             
                                                                (@@@@@@@@@@@@@@@@@@@@@@@@@@@                         
                                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@                      
                                                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                   
                                                                 ,@@@@@@@.  /@@@@@@@@@@@@@@@@@@@@@%                  
                                                                @@@@@@@&     @@@@@@@@@@@@@@@@@@@@@@%                 
                                                             .@@@@@@@@&       @@@@@@@@@@@@@@@@@@@@@@                 
                                                           #@@@@@@@@@@         @@@@@@@@@@@@@@@@@@@@@/                
                                                        *@@@@@@@@@@@@@          .@@@@@@@@@@@@@@@@@@@.                
                                                     %@@@@@@@@@@@@@@@@%            %@@@@@@@@#   @@@@                 
                                                 &@@@@@@@@@@@@@@@@@@@@@@           ,@@@        .@@@                  
                                                &@@@@@@@@@@@@@@@@@@@@@@@@@@&##%@@@@@@@@@%     @@@@                   
                                                       %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&                    
                                                         /@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      
                                                          %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/                       
                                                           (@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@(                         
                                                              %@@@@@@@@@@@@@@@@@@@@@@@@@@,                           
                                                                        #@@@@@@@@@@@@@%                              
                                                                          #@@@@@@@@#                                 
                                                                           @@@@&                                     


                                            ▓█████▄   ▒█████    ███▄    █  ▄▄▄█████▓    █     █░ ▒█████   ██▀███    ██▀███  ▓██   ██▓
                                            ▒██▀ ██▌ ▒██▒  ██▒  ██ ▀█   █  ▓  ██▒ ▓▒   ▓█░ █ ░█░▒██▒  ██ ▓██ ▒ ██ ▒▓██ ▒ ██ ▒▒██  ██▒
                                            ░██   █▌ ▒██░  ██▒ ▓██  ▀█ ██▒ ▒ ▓██░ ▒░   ▒█░ █ ░█ ▒██░  ██ ▓██ ░▄█  ▒▓██ ░▄█  ▒ ▒██ ██░
                                            ░▓█▄   ▌ ▒██   ██░ ▓██▒  ▐▌██▒ ░ ▓██▓ ░    ░█░ █ ░█ ▒██   ██ ▒██▀▀█▄   ▒██▀▀█▄    ░ ▐██▓░
                                            ░▒████▓  ░ ████▓▒░ ▒██░   ▓██░   ▒██▒ ░    ░░██▒██▓ ░ ████▓▒ ░██▓ ▒██ ▒░██▓ ▒██ ▒ ░ ██▒▓░
                                             ▒▒▓  ▒  ░ ▒░▒░▒░  ░ ▒░   ▒ ▒    ▒ ░░      ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓ ░░ ▒▓ ░▒▓ ░  ██▒▒▒ 
                                             ░ ▒  ▒    ░ ▒ ▒░  ░ ░░   ░ ▒░     ░         ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒ ░  ░▒ ░ ▒ ░▓██ ░▒░ 
                                             ░ ░  ░  ░ ░ ░ ▒      ░   ░ ░    ░           ░   ░  ░ ░ ░ ▒    ░░   ░    ░░   ░  ▒ ▒ ░░  
                                               ░         ░ ░           ░                  ░        ░ ░     ░        ░      ░ ░     
                                             ░                                                                          ░ ░     

'''

print(banner)
                                                                             
                                                                            
import websocket
import json
import threading
import time
import requests

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def recieve_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    print(" LISTENING ")
    while True:
        time.sleep(interval)
        heartbeatJSON = {"op": 1, "d": "null"}
        send_json_request(ws, heartbeatJSON)

def send_to_discord_webhook(content):
    webhook_url = "YOUR_HOOK_HERE" # YOUR DISCORD WEB HOOK URL
    data = {
        "content": content
    }
    requests.post(webhook_url, json=data)

def websocket_loop():
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")
    event = recieve_json_response(ws)

    heartbeat_intervals = event['d']['heartbeat_interval'] / 1000
    print("heartbeat_intervals = ", heartbeat_intervals)
    threading._start_new_thread(heartbeat, (heartbeat_intervals, ws))

    token = "YOUR_TOKEN_HERE"  # YOUR ACCOUNT TOKEN
    payload = {'op': 2, "intents": 513, 'd':{"token": token, "properties": {"$os": "windows", "$browser": "chrome", "$device": "pc"}}}
    send_json_request(ws, payload)

    while True:
        event = recieve_json_response(ws)
        try:
            if event and 'd' in event and 'author' in event['d']:
                message_content = event['d']['content']
                author_username = event['d']['author']['username']

                server_id = event['d'].get('guild_id')
                server_name = "DM"
                if server_id:
                    server_name = event['d'].get('guild', {}).get('name', 'Unknown Server')

                print(f"{author_username} ({server_name} - {server_id}): {message_content}")

                op_code = event['op']
                if op_code == 11:
                    print('heartbeat received')

                if server_name == "DM":
                    with open('DM_messages.txt', 'a') as dm_file:
                        dm_file.write(f"{author_username} ({server_name} - {server_id}): {message_content}\n")
                else:
                    with open('Server_messages.txt', 'a') as server_file:
                        server_file.write(f"{author_username} ({server_name} - {server_id}): {message_content}\n")

                send_to_discord_webhook(f"{author_username} ({server_name} - {server_id}): {message_content}")

        except Exception as e:
            #print(f"Error: {str(e)}")
            pass

if __name__ == "__main__":
    websocket_loop()
