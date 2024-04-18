from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent

CARD_TEMPLATE = """
<div class="col p-2">
            <div class="card" style="width: 18rem;">
              <div class="card-body">
                <h5 class="card-title">Из {from_country}</h5>
                <h5 class="card-title">В {to_country}</h5>
                <h6 class="card-subtitle mb-2 text-body-secondary">Время полета: {fly_time}</h6>
                <p class="card-text">Дата рейса: {flight_date}</p>
                <p class="card-text">Дата обратного рейса: {back_date}</p>
                  <h3>Цена: {price}</h3>
                <a href="#" class="card-link"><button type="button" class="btn btn-info" style="background-color: #588c8b !important; border-color: #588c8b">Забронировать</button></a>
              </div>
            </div>
        </div>
"""


class Ticket:
    def __init__(self, **kwargs):
        self.from_country = kwargs.get("from_country")
        self.to_country = kwargs.get('to_country')
        self.price = kwargs.get("price")
        self.time = kwargs.get('time')
        self.flight_date = kwargs.get("flight_date")
        self.back_date = kwargs.get("back_date")
        self.fly_time = kwargs.get("fly_time")
        self.allowed = True

    def fill_html(self):
        return CARD_TEMPLATE.format(**self.__dict__)


class KayakTicketParser:
    def __init__(self, link=None):
        if not link:
            self.link = "https://www.kayak.com/flight-routes/Atlanta-Hartsfield-Jackson-ATL/New-York-LaGuardia-LGA"
        self.tickets_list = []

    def run(self):
        response = requests.get(self.link)
        bs = BeautifulSoup(response.text, 'lxml')
        buttons = bs.findAll('div', attrs={"class": 'xl4G'})
        for button in buttons:
            data = {}
            from_country, to_country = "Atlanta-Hartsfield-Jackson", "New-York-LaGuardia"
            fly_time = button.find("div", attrs={"class": 'xl4G-info-column xl4G-mod-large'}).\
                find("span", attrs={"class": "xl4G-primary-text"}).text
            price = button.find("div", attrs={"class": "xl4G-price-wrapper"}).find("span", attrs={"class": 'xl4G-price'}).text
            flight_date, back_date = map(str.strip, button.find('div', attrs={"class": "xl4G-operational-wrapper"}).text.split("-"))
            data.update({"from_country": from_country,
                         "to_country": to_country,
                         'fly_time': fly_time,
                         'price': price,
                         'flight_date': flight_date,
                         'back_date': back_date})
            self.tickets_list.append(Ticket(**data))
        cards = ''
        for ticket in self.tickets_list:
            cards += ticket.fill_html()

        print(cards)
        with open(BASE_DIR / 'avia_ticket_sales' / 'templates'/ 'avia_ticket_sales' / 'cards.html', 'w', encoding='utf-8') as file:
            file.write("{% extends 'avia_ticket_sales/layout.html' %}")
            file.write("{% load static %}")
            file.write("{% block content %}")
            file.write(cards)
            file.write("{% endblock %}")


a = KayakTicketParser()
print(a.run())