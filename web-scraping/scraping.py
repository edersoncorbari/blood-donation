import requests
import json
import datetime

from bs4 import BeautifulSoup
from utils import *


class BloodScraping(object):

    __site = 'http://www.prosangue.sp.gov.br/home/Default.html'

    def __init__(self):
        self.html = requests.get(self.__site).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.update = dt_utc_format(
            tz_to_utc(
                datetime.datetime.strptime(
                    iso_dt_format(
                        self.soup.find(
                            class_='caixa pt-BR').p.text),
                    '%Y-%m-%d %H:%M:%S')))
        self.stock = self.soup.find(class_='estoque')
        self.timestamp = dt_utc_format(tz_to_utc(datetime.datetime.now()))

    def getPosition(self):
        return self.__prepareData()

    def numStatus(self, status: str) -> int:
        if status == 'critico':
            return 0
        elif status == 'emergencia':
            return 1
        elif status == 'estavel':
            return 2
        else:
            raise Exception('No found type of status...')

    def __prepareData(self):
        # 1. O+
        b1 = {
            "blood": "O+",
            "status": self.numStatus(
                self.stock.find(
                    id="cphConteudo_Estoque1_Repeater1_lblO_0")['class'][0]),
            "update": self.update,
            "timestamp": self.timestamp}

        # 2. A+
        b2 = {
            "blood": "A+",
            "status": self.numStatus(
                self.stock.find(
                    id="cphConteudo_Estoque1_Repeater1_lblO_1")['class'][0]),
            "update": self.update,
            "timestamp": self.timestamp}

        # 3. AB+
        b3 = {
            "blood": "AB+",
            "status": self.numStatus(
                self.stock.find(
                    id='cphConteudo_Estoque1_Repeater1_lblO_2')['class'][0]),
            "update": self.update,
            "timestamp": self.timestamp}

        # 4. B+
        b4 = {
            "blood": "B+",
            "status": self.numStatus(
                self.stock.find(
                    id='cphConteudo_Estoque1_Repeater1_lblO_3')['class'][0]),
            "update": self.update,
            "timestamp": self.timestamp}

        # 5. O-
        b5 = {
            "blood": "O-",
            "status": self.numStatus(
                self.stock.find(
                    id='cphConteudo_Estoque1_Repeater1_lblO_4')['class'][0]),
            "update": self.update,
            "timestamp": self.timestamp}

        # 6. A-
        b6 = {
            "blood": "A-",
            "status": self.numStatus(
                self.stock.find(
                    id='cphConteudo_Estoque1_Repeater1_lblO_5')['class'][0]),
            "update": self.update,
            "timestamp": self.timestamp}

        # 7. AB-
        b7 = {
            "blood": "AB-",
            "status": self.numStatus(
                self.stock.find(
                    id='cphConteudo_Estoque1_Repeater1_lblO_6')['class'][0]),
            "update": self.update,
            "timestamp": self.timestamp}

        # 8. B-
        b8 = {
            "blood": "B-",
            "status": self.numStatus(
                self.stock.find(
                    id='cphConteudo_Estoque1_Repeater1_lblO_7')['class'][0]),
            "update": self.update,
            "timestamp": self.timestamp}

        bloods = (b1, b2, b3, b4, b5, b6, b7, b8)
        return json.loads(json.dumps(bloods))
