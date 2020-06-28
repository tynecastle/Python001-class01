import requests
from bs4 import BeautifulSoup as bs
import lxml.etree
from time import sleep
import re
import pandas as pd

url_home = 'https://maoyan.com'
url_films = f'{url_home}/films?showType=3'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Connection": "keep-alive",
    "Cookie": "uuid_n_v=v1; uuid=77283BD0B92711EA9736CB82F1E06989EB9C91943718433895E6609099BBF979; _csrf=9546e502d34e6dfa99268cb6b16791c23a6823ee994a8cba2a70412cc4ba234d; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593338975; _lxsdk_cuid=172fa6755c099-0a4b8052451fbd-31637403-232800-172fa6755c1c8; _lxsdk=77283BD0B92711EA9736CB82F1E06989EB9C91943718433895E6609099BBF979; mojo-uuid=64e64b593a123b8ee8553377074055f0; mojo-session-id={\"id\":\"d37dd3b3d50271fa8a7d159424659d5b\",\"time\":1593354574536}; mojo-trace-id=2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593356062; __mta=217545385.1593338975830.1593354574789.1593356061880.4; _lxsdk_s=172fb5546a6-c7-7b9-54%7C%7C6",
    "Upgrade-Insecure-Requests": "1",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
}
output_file = './maoyan_top10.csv'

def write_data(content):
    film = pd.DataFrame(data=content)
    film.to_csv(output_file, mode='a', encoding='utf8', index=False, header=False)

def get_film_details(url):
    response = requests.get(url, headers=headers)
    selector = lxml.etree.HTML(response.text)
    film = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/h1/text()')
    film_name = film[0]
    film_type = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/*/text()')
    plan_date = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()')
    plan_date = re.sub(r'[^\d-]', '', plan_date[0])
    write_data([film_name, film_type, plan_date])

def retrieve_films():
    response = requests.get(url_films, headers=headers)
    soup = bs(response.text, 'html.parser')
    soup_conetnt = soup.find_all("div", attrs={'class': 'movie-item film-channel'})
    for i in soup_conetnt[0:10]:
        get_film_details(url_home + i.find('a').get('href'));
        sleep(5)

if __name__ == '__main__':
    retrieve_films()
