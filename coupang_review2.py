import requests
from bs4 import BeautifulSoup

product_id = ''

url = 'https://www.coupang.com/vp/product/reviews'
header = {
    'Referer': f'https://www.coupang.com/vp/products/{product_id}?isAddedCart=',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'cookie': ''
}

page = 1

params = {
    'productId': product_id,
    'page': page,
    'size': 100,
    'sortBy': 'ORDER_SCORE_ASC',
    'ratings': None,
    'q': None,
    'viRoleCode': 3,
    'ratingSummary': 'true',
}

response = requests.get(url=url, params=params, headers=header)

soup = BeautifulSoup(response.text, 'html.parser')
total_review_count = soup.select('div.sdp-review__article__list__hidden-rating')[1].attrs['data-review-total-count']
soup.select('div.sdp-review__article__list__info') # for문 돌리면 되겠다.