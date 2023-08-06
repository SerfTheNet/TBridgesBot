from bs4 import BeautifulSoup
import requests
import base64

brigdes_url = 'https://bridges.torproject.org/bridges?transport=obfs4'

proxies = {}
# proxies = {
#     'https': 'socks5://localhost:1080'
# }

def getCapcha():
    res_page = requests.get(brigdes_url, proxies=proxies)
    bs = BeautifulSoup(res_page.text, features='html.parser')

    img_data = bs.find('div', attrs={'id':'bridgedb-captcha'},
        ).img.attrs['src'].split(',')[1]    
    captcha_code = bs.find('input', attrs={'name': 'captcha_challenge_field'}).attrs['value']

    img_bin = base64.decodebytes(bytes(img_data, 'utf-8'))

    return img_bin, captcha_code


def sendCode(captcha_code, capcha_value):
    bridges_page = requests.post(
        'https://bridges.torproject.org/bridges',
        params={'transport': 'obfs4'},
        headers={'Origin': 'null', 'Referer': None},
        data={
            'captcha_challenge_field': captcha_code,
            'captcha_response_field': capcha_value,
            'submit': 'submit',
        },
        proxies=proxies
    )
    
    bridges = BeautifulSoup(bridges_page.text).find(id = 'bridgelines').text
    return bridges