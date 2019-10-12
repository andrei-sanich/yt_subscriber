import requests
import pickle
import datetime
from main import send_message


def pubsubhubbub_handler(channel_id, mode='subscribe'):

    url = 'https://pubsubhubbub.appspot.com/subscribe'
    querystring = {
        'hub.callback': 'https://test.pythonanywhere.com/',
        'hub.topic': 'https://www.youtube.com/xml/feeds/videos.xml?channel_id={}'.format(channel_id),
        'hub.mode': mode,
        'hub.verify': 'async',
        'hub.lease_seconds': 691200
        }

    requests.request('POST', url, params=querystring)


def main():

    with open('data.pickle', 'rb') as f:
        channel_ids = pickle.load(f)

    for channel_id in channel_ids:
        pubsubhubbub_handler(channel_id)


if __name__  == '__main__':

    today = datetime.date.today()
    weekday = today.weekday()
    if (weekday == 1):
        main()
        
