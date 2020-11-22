from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import os
import zipfile



def repairs_data():
    way = os.path.abspath('repairs.py').replace('repairs.py', 'data.zip')
    s = urlopen('https://data.mos.ru/opendata/7701236617-zaplanirovannye-dorojnye-remontnye-raboty-na-2020-god').read().decode('utf-8')
    data = str(s)
    soup = BeautifulSoup(data, 'html.parser')
    a = soup.find_all('a', href=True, onclick="incDownloadCounter(62101); sndMosruMsgFromPassport('setdownload', 62101);")[0]

    f=open(way, "wb") #открываем файл для записи, в режиме wb
    ufr = requests.get('http:' + a['href']) #делаем запрос
    f.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
    f.close()

    fantasy_zip = zipfile.ZipFile(os.path.abspath('data.zip'))
    fantasy_zip.extractall(os.path.abspath('repairs.py').replace('repairs.py', ''))

    os.remove(os.path.abspath('repairs.py').replace('repairs.py', 'data-108554-2020-11-20.xlsx'))
    fantasy_zip.close()


repairs_data()