import pytz
from django.db import models
from django.core.validators import RegexValidator


class Mailing(models.Model):
    time_start = models.DateTimeField(verbose_name='Время запуска рассылки')
    time_end = models.DateTimeField(verbose_name='Время окончания рассылки')
    text = models.TextField(max_length=255, verbose_name='Текст сообщения')
    tag = models.CharField(max_length=100, verbose_name='Тэг клинта', blank=True)
    mob_operator = models.CharField(verbose_name='Мобильный оператор клиента',
                                    max_length=3, blank=True)

    def __str__(self):
        return 'Рассылка {} текст: {} время: {}'.format(self.id, self.text, self.time_start)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_regex = RegexValidator(regex=r'^7\d{10}$',
                                 message="номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)")
    phone_number = models.CharField(verbose_name='Номер телефона', validators=[phone_regex], unique=True, max_length=11)
    mob_operator = models.CharField(verbose_name='Мобильный оператор', max_length=3, editable=False)
    tag = models.CharField(verbose_name='Тэг', max_length=100, blank=True)
    timezone = models.CharField(verbose_name='Часовой пояс', max_length=32, choices=TIMEZONES, default='UTC')

    def save(self, *args, **kwargs):
        self.mobile_operator_code = str(self.phone_number)[1:4]
        return super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return 'Клиент {}, +7({}){}-{}-{}'.format(self.id, self.phone_number[1:4], self.phone_number[4:7],
                                                  self.phone_number[7:9], self.phone_number[9:11])

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    SENT = "sent"
    NO_SENT = "no sent"

    STATUS_CHOICES = [
        (SENT, "Отправлено"),
        (NO_SENT, "Не отправлено"),
    ]

    created_at = models.DateTimeField(verbose_name='Дата-время создания', auto_now_add=True)
    sending_status = models.CharField(verbose_name='Статус отправки', max_length=15, choices=STATUS_CHOICES)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return '{} сообщение: {}, клиент: {}'.format(self.id, self.mailing, self.client)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


mg = Mailing()
