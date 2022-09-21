import os
import time
import requests
import datetime
from dotenv import load_dotenv
import pytz

from celery.utils.log import get_task_logger
from .data import find_mailings_time, get_clients, save_message, get_message
from message_service.celery import app

logger = get_task_logger(__name__)

load_dotenv()

URL = os.environ.get('URL ', os.getenv('URL')).strip()
TOKEN = os.environ.get('TOKEN ', os.getenv('TOKEN')).strip()


@app.task
def db_queries():
    mails_data = find_mailings_time()
    for item in mails_data:
        print('Новая рассылка: {} - {} - {}'.format(item.id, item.time_start, item.text))
        clients = get_clients(item.tag, item.mob_operator)
        for client in clients:
            tz = pytz.timezone(client.timezone)
            i_dict = dict(id_m=item.id,
                          time_start=item.time_start.replace(tzinfo=pytz.utc).astimezone(tz),
                          time_end=item.time_end.replace(tzinfo=pytz.utc).astimezone(tz),
                          text=item.text,
                          tag=item.tag,
                          mob_operator=item.mob_operator,
                          id_c=client.id,
                          phone=client.phone_number,
                          timezone=client.timezone,
                          )
            to_send = dict(text=item.text,
                           phone=int(client.phone_number),
                           )
            send_message.delay(i_dict, to_send, item.time_start.strftime('%S'))

    return 'опрос бд на наличие новых рассылок'


@app.task
def send_message(data, data_to_send, time_seconds):
    time_to_send = int(time_seconds) - int(datetime.datetime.now().strftime('%S'))
    if time_to_send < 0: time_to_send = 0
    time.sleep(time_to_send)
    tz = pytz.timezone(data['timezone'])
    time_start = datetime.datetime.strptime(data['time_start'], '%Y-%m-%dT%H:%M:%S%z')
    time_end = datetime.datetime.strptime(data['time_end'], '%Y-%m-%dT%H:%M:%S%z')
    time_now_str = datetime.datetime.strftime(datetime.datetime.now(tz), '%Y-%m-%d %H:%M:%S%z')
    time_now = datetime.datetime.strptime(time_now_str, '%Y-%m-%d %H:%M:%S%z')

    if time_start <= time_now <= time_end:
        try:
            data_to_send['id'] = get_message()
        except:
            data_to_send['id'] = 1
        header = {'Authorization': f'Bearer {TOKEN}',
                  'Content-Type': 'application/json'}
        response = requests.post(url=URL + str(data_to_send['id']), headers=header, json=data_to_send)
        if response.status_code == 200:
            data['status'] = "sent"
        else:
            data['status'] = "no sent"
        result = response.json()['message']
    else:
        data['status'] = "no sent"
        result = 'Time out'
    save_message(data)
    return result
