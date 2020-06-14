from django.conf import settings
from django.core.mail import send_mail

from eventservice.models import Event
from datetime import datetime, timedelta

def SendMail(title, msg, toemail):
    if not isinstance(toemail, list):
        toemail = [toemail]
    return send_mail(title, msg, settings.EMAIL_HOST_USER, toemail)

def sender_email():
    events = Event.get(all=True, alerted=False, date_appointed__lte=datetime.now() + timedelta(hours=1))
    if events is None:
        print('Ничего нет')
    else:
        for event in events:
            print('Отправляю сообщение!') #Сообщение отправляется дважды по причине того, что активне Debug
            SendMail('Скоро что-то произойдёт..', f'Менее чем через час у вас должно произойти событие с наименованием "{event.title}"', event.user.email)
            event.update(alerted=True)
    