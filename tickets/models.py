import uuid

from django.db import models


CARD_TEMPLATE = """
<div class="col p-2">
            <div class="card shadow rounded" style="width: 22rem; card-box-shadow: 1px">
              <div class="card-body">
                <h5 class="card-title">Из {from_country}</h5>
                <h5 class="card-title">В {to_country}</h5>
                <h6 class="card-subtitle mb-2 text-body-secondary">Время полета: {fly_time}</h6>
                <p class="card-text">Дата рейса: {flight_date}</p>
                <p class="card-text">Дата обратного рейса: {back_date}</p>
                  <h3>Цена: {price}</h3>
                <a href="#" class="card-link"><button type="button" class="btn btn-info" style="background-color: #588c8b !important; border-color: #588c8b; color: white">Забронировать</button></a>
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
    ticket_uid = models.UUIDField(default=uuid.uuid4, primary_key=True)

    def fill_html(self):
        return CARD_TEMPLATE.format(**self.__dict__)

