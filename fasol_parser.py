import datetime
import csv
import requests
import aiohttp
import asyncio
import aiofiles
from aiocsv import AsyncWriter
import tracemalloc
from bs4 import BeautifulSoup

tracemalloc.start()

current_date = datetime.datetime.now().strftime('%m-%d')

with open(f'fasol_{current_date}.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(
        (
            'Продукт',
            'Новая цена',
            'Старая цена',
            'Процент скидки',
        )
    )


async def all_tovar_str(page):

    headers = {
        'authority': 'myfasol.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7,application/json',
        'accept-language': 'ru,en;q=0.9',
        'referer': f'https://myfasol.ru/promotions/?PAGEN_1={page}',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
    }

    async with aiohttp.ClientSession() as session:

        response = await session.get(f'https://myfasol.ru/promotions/?PAGEN_1={page}', headers=headers)

        j = await response.text()


        return j



async def products_str(j):

    soup = BeautifulSoup(j, 'lxml')

    products = soup.find_all('div', class_='col-6 col-md-4 col-xl-3 actions__col')

    for product in products:
        if product.find('div', class_='actions__item--oldprice'):
            name = product.find('div', class_='actions__item--title').text

            price = product.find('div', class_='actions__item--price').text.replace('i/шт', '')

            oldprice = product.find('div', class_='actions__item--oldprice').text.replace('i/шт', '')

            sale = f'{round((1 - float(price) / float(oldprice)) * 100)}%'

            async with aiofiles.open(f'fasol_{current_date}.csv', 'a', encoding='utf-8', newline='') as file:
                writer = AsyncWriter(file)

                await writer.writerow(
                    (
                        name,
                        price,
                        oldprice,
                        sale,
                    )
                )





async def fasol_main():
    headers = {
        'authority': 'myfasol.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7,application/json',
        'accept-language': 'ru,en;q=0.9',
        'referer': 'https://myfasol.ru/promotions/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
    }

    response = requests.get(
        'https://myfasol.ru/promotions/',
        headers=headers
    )
    soup = BeautifulSoup(response.text, 'lxml')


    lists = soup.find_all('li', class_='page-item')[-2].text

    for page in range(1, int(lists)+1):
        result_str = await all_tovar_str(page)
        await products_str(result_str)

    return f'fasol_{current_date}.csv'


if __name__ == '__main__':
    asyncio.run(fasol_main())