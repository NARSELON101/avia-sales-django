import uuid

from django.contrib.auth.models import User
from django.db import models


CARD_TEMPLATE_ALLOWED = """
<div class="col p-2">
            <div class="card shadow rounded" style="width: 22rem; card-box-shadow: 1px">
              <div class="card-body">
                <h5 class="card-title">Из {from_country}</h5>
                <h5 class="card-title">В {to_country}</h5>
                <h6 class="card-subtitle mb-2 text-body-secondary">Время полета: {fly_time}</h6>
                <p class="card-text">Дата рейса: {flight_date}</p>
                <p class="card-text">Дата обратного рейса: {back_date}</p>
                  <h3>Цена: {price}</h3>
                <a href="{url_string}" class="card-link"><button type="button" class="btn btn-info" style="background-color: #588c8b !important; border-color: #588c8b; color: white">Забронировать</button></a>
              </div>
            </div>
        </div>
"""


CARD_TEMPLATE_DISABLED = """
<div class="col p-2">
            <div class="card shadow rounded" style="width: 22rem; card-box-shadow: 1px">
              <div class="card-body">
                <h5 class="card-title">Из {from_country}</h5>
                <h5 class="card-title">В {to_country}</h5>
                <h6 class="card-subtitle mb-2 text-body-secondary">Время полета: {fly_time}</h6>
                <p class="card-text">Дата рейса: {flight_date}</p>
                <p class="card-text">Дата обратного рейса: {back_date}</p>
                  <h3>Цена: {price}</h3>
                <button type="button" class="btn btn-info" style="background-color: gray !important; border-color: gray; color: white; cursor: not-allowed; pointer-events: none;">Недоступно</button>
              </div>
            </div>
        </div>
"""


class Ticket(models.Model):
    from_country = models.CharField(max_length=30)
    to_country = models.CharField(max_length=30)
    price = models.CharField(max_length=30)
    fly_time = models.CharField(max_length=30)
    flight_date = models.CharField(max_length=30)
    back_date = models.CharField(max_length=30)
    allowed = models.BooleanField(default=True, max_length=30)
    user_model = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    ticket_uid = models.UUIDField(default=uuid.uuid4, primary_key=True)

    def fill_html(self):
        if self.user_model:
            return CARD_TEMPLATE_DISABLED.format(**self.__dict__)
        else:
            url_string = "{{% url 'ticket_reserve' '{0}' %}}".format(self.ticket_uid)
            return CARD_TEMPLATE_ALLOWED.format(url_string=url_string, **self.__dict__)

