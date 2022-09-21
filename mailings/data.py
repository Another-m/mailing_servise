import pytz
from django.db.models import Q

from mailings.models import Mailing, Client, Message
from datetime import datetime

from message_service.settings import TIME_ZONE


def find_mailings_time():
    d_time = datetime.now(pytz.timezone(TIME_ZONE))
    data = Mailing.objects.filter(time_start__year=d_time.year,
                                  time_start__month=d_time.month,
                                  time_start__day=d_time.day,
                                  time_start__hour=d_time.hour,
                                  time_start__minute=d_time.minute,
                                  ).order_by('time_start').all()
    return data

def get_clients(tag, operator_code):
    data = Client.objects.filter(Q(mob_operator=operator_code) | Q(tag=tag)).all()
    # data = [{'id': i.id, 'phone_number': i.phone_number, 'timezone': i.timezone} for i in data]
    return data


def save_message(data):
    Message.objects.create(
                    sending_status=data["status"],
                    client_id=data["id_c"],
                    mailing_id=data["id_m"],
                )


def get_message():
    return int(Message.objects.latest('id').id) + 1



