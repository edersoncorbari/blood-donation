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

    def bloodType(self, index) -> int:
        return ['O+', 'A+', 'AB+', 'B+', 'O-', 'A-', 'AB-', 'B-'][index]

    def __prepareData(self):
        bloods = []
        element = 'cphConteudo_Estoque1_Repeater1_lblO_'

        for i in range(8):
            bloods.append(
                {'blood': self.bloodType(i),
                 'status': self.numStatus(self.stock.find(id=element + str(i))['class'][0]),
                 'update': self.update, 'timestamp': self.timestamp})

        return json.loads(json.dumps(bloods))
