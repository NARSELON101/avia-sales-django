from pathlib import Path

import requests
from bs4 import BeautifulSoup

from tickets.models import Ticket

BASE_DIR = Path(__file__).resolve().parent


class KayakTicketParser:
    def __init__(self, link=None):
        if not link:
            self.link = "https://www.kayak.com/flight-routes/Atlanta-Hartsfield-Jackson-ATL/New-York-LaGuardia-LGA"

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
                         'price': price,
                         'fly_time': fly_time,
                         'flight_date': flight_date,
                         'back_date': back_date})
            tickets = Ticket.objects.values()
            no_uid_tickets = []

            data.update({'allowed': True})

            for ticket in tickets:
                no_uid_tickets.append({key: value for key, value in ticket.items() if key not in ['ticket_uid',
                                                                                                  'user_model_id',
                                                                                                  'is_notified']})
            new_ticket = Ticket(**data)

            if data not in no_uid_tickets:
                new_ticket.save()

        cards = ''
        all_tickets = Ticket.objects.all()

        for ticket in all_tickets:
            cards += ticket.fill_html()

        with open(BASE_DIR / 'avia_ticket_sales' / 'templates' / 'avia_ticket_sales' / 'cards.html', 'w',
                  encoding='utf-8') as file:
            file.write("{% extends 'avia_ticket_sales/tickets.html' %}\n")
            file.write("{% load static %}\n")
            file.write("{% block content1 %}\n")
            file.write(cards)
            file.write("{% endblock %}")


def main():
    KayakTicketParser().run()
