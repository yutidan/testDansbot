import requests
from time import sleep

url = "https://api.telegram.org/bot439793417:AAF43mx235BM_hYayKwW2o9-sxpAo42muu4/"


def get_updates_json(request, timeout=100, offset=None):  
    params = {'timeout': timeout, 'offset': offset}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()

def last_update(data):  
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]
    
def get_chat_id(update):  
    chat_id = update['message']['chat']['id']
    return chat_id

def send_stmess(chat, text, keyb=None):  
    params = {'chat_id': chat, 'text': text, 'reply_markup': keyb}
    response = requests.post(url + 'sendMessage', json=params)
    return response

def send_mess(chat, text):  
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

def send_sticker(chat, sticker='CAADAgADQQoAApkvSwqnrw2BEeUQJwI'): 
    params = {'chat_id': chat, 'sticker':sticker}
    response = requests.post(url + 'sendSticker', data=params)
    return response
    
def get_weather(id=524901):
    appid="4402690737920e1e52195392c87dc597"
    params={"id": id, "appid": appid}
    response=requests.get("http://api.openweathermap.org/data/2.5/weather", params=params)
    return response.json()
    
 def main():  
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
        data=last_update(get_updates_json(url))
        if update_id == data['update_id']:
            name=data['message']['chat']['first_name']
            if 'text' in data['message']:
                if data['message']['text'] == '/start':
                    ttt='Hello, '
                    keyb={"keyboard":[[{"text":"Weather"}]], "resize_keyboard": True}
                    send_stmess(get_chat_id(data), ttt+name, keyb)
                    update_id += 1
                elif data['message']['text'] == 'Weather':
                    weather=get_weather()
                    send_mess(get_chat_id(data), 'Here it is, {}. \n The temperature in {} is {}'.format(name, weather['name'],str(round(weather['main']['temp']-273))))
                    update_id += 1
                else:
                    send_mess(get_chat_id(data), 'I can\'t do anything more for you, '+name)
                    update_id += 1
            elif 'sticker' in data['message']:
                send_sticker(get_chat_id(data))
                update_id += 1
            else:
                send_mess(get_chat_id(data),'What have you sent me, dumbass?')
                update_id += 1
                
    sleep(5)       

if __name__ == '__main__':  
    main()
