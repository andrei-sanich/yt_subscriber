from flask import (
    Flask,
    request
    )
from flask_sslify import SSLify
import pathlib
import pickle
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import requests
from script import pubsubhubbub_handler
import config


app = Flask(__name__)
sslify = SSLify(app)
path = pathlib.Path('data.pickle')


def send_message(chat_id=config.CHAT_ID, text):

    url = '{}/{}:{}/{}sendMessage'.format(
        congig.TELEGRAM_URL,
        config.BOT_ID,
        config.TOKEN
        )
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)

    return r.json()


def get_channel_id(url):

    url_channel = urlparse(url)
    path = url_channel.path.split('/')
    if url_channel.scheme == 'https' and (
        url_channel.netloc == 'youtube.com' or url_channel.netloc == 'www.youtube.com'
        ) and path[1] == 'channel':
        
        return path[2]


def add_channel_id(channel_id):

    if not path.exists():
        list_channel_ids = []
        list_channel_ids.append(channel_id)
        with open('data.pickle', 'wb') as f:
            pickle.dump(list_channel_ids, f)
    else:
        with open('data.pickle', 'rb') as f:
            channel_ids = pickle.load(f)
        if channel_id not in channel_ids:
            channel_ids.append(channel_id)
            with open('data.pickle', 'wb') as f:
                pickle.dump(channel_ids, f)
    

@app.route('/incoming', methods=['POST', 'GET'])
def incoming():
    
    if request.method == 'GET':
        response = request.args['hub.challenge']
        if response:

            return response

    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = request.get_json()
            if 'edited_message' in data:

                return 'Bot welcomes you'

            message = data['message']['text']
            if message == '/start':
                answer = 'Я буду отправлять тебе уведомления c youtube'
                send_message(my_chat_id, text=answer)
            else:
                channel_id = get_channel_id(message)
                if channel_id:
                    add_channel_id(channel_id):
                    pubsubhubbub_handler(channel_id)
                    send_message(my_chat_id, text='Подписка на канал завершена')

            return 'Bot welcomes you'

        if request.content_type == 'application/atom+xml':
            data = request.get_data()
            root = ET.fromstring(data)
            youtube_video_link = root[4][4].get('href')
            if youtube_video_link:
                send_message(my_chat_id, text=youtube_video_link)
    
    return '<h1>Bot welcomes you</h1>'


if __name__  == '__main__':
    app.run()

