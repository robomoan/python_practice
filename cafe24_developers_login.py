import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

'''
Cafe24 Developers 페이지 로그인 구현
URL: https://developers.cafe24.com/ko
Author: bhroh
Tools used: Chrome, Fiddler Classic
'''

load_dotenv()
id = os.getenv('CAFE24ID')
pw = os.getenv('CAFE24PW')

# Login Phase 1
url_1 = 'https://developers.cafe24.com/developer/rest/login'
body_1 = {
    'loginId': id,
    'loginPasswd': pw
}
res_1 = requests.post(url=url_1, data=body_1)
encData = res_1.json()['sEncData']
encKey = res_1.json()['sEncKey']
cookie_dict_1 = res_1.cookies.get_dict()


# Login Phase 2
url_2 = 'https://user.cafe24.com/comLogin/?action=comLogin'
header_2 = {
    'Referer': 'https://developers.cafe24.com/',
    'Content-Type': 'application/x-www-form-urlencoded'
}
body_2 = {
    'EncData': encData,
    'EncKey': encKey,
    'loginId': id,
    'loginPasswd': pw
}
res_2 = requests.post(url=url_2, data=body_2)
soup_2 = BeautifulSoup(res_2.text)
body_3: dict[str, str] = {x.attrs['name']: x.attrs['value'] for x in soup_2.select('form > input')}

cookie_dict_2 = res_2.cookies.get_dict()
cookie = ';'.join(
    [ ';'.join([ key + '=' + value for key, value in zip(cookie_dict_1.keys(), cookie_dict_1.values())]),
      ';'.join([ key + '=' + value for key, value in zip(cookie_dict_2.keys(), cookie_dict_2.values())]) ]
)


# Login Phase 3
url_3 = 'https://cuid-sso.wehost24.com/mc3.php'
header_3 = {
    'Referer': 'https://user.cafe24.com/',
    'Content-Type': 'application/x-www-form-urlencoded'
}
res_3 = requests.post(url=url_3, data=body_3, headers=header_3)
soup_3 = BeautifulSoup(res_3.text)
url_4: str = soup_3.select("script[type='text/javascript']")[0].text[25:-2]


# Login Phase 4
header_4 = {
    'Referer': 'https://cuid-sso.wehost24.com/',
    'Cookie': cookie
}
res_4 = requests.get(url=url_4, headers=header_4)


# Login Phase 5
url_5 = 'https://developers.cafe24.com/admin/front/main'
header_5 = {
    'Referer': url_4,
    'Cookie': cookie
}
res_5 = requests.get(url=url_5, headers=header_5)
print(res_5.text)
