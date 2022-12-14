import requests
from bs4 import BeautifulSoup


url = 'https://www.coupang.com/np/products/brand-shop'
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'cookie': ''
}

page = 1
total_page = 1
soup_product_codes = []

while page <= total_page:
    params = {
        'brandName': '',
        'page': page
    }
    response = requests.get(url=url, params=params, headers=header)

    if page == 1:
        total_page: int = len(soup.select('div.page-warpper')[0].find_all('a'))

    soup = BeautifulSoup(response.text, 'html.parser')
    soup_tags = soup.select('li.baby-product')
    soup_product_codes.extend([tag.attrs['data-product-id'] for tag in soup_tags])

    page += 1

soup.select('div.page-warpper')[0].find_all('a')
#product-list-paging > div > a.icon.next-page-dimmed