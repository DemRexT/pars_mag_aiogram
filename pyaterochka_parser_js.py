import datetime
import csv
import aiohttp
import asyncio
import aiofiles
from aiocsv import AsyncWriter
import tracemalloc

tracemalloc.start()

current_date = datetime.datetime.now().strftime('%m-%d')

with open(f'pyaterochka_{current_date}.csv', 'w', encoding='utf-8', newline='') as file:
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
        'authority': '5ka.ru',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9',
        'referer': 'https://5ka.ru/special_offers/?page=3',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
    }

    params = {
        'records_per_page': '15',
        'page': page,
        'store': '5642',
        'ordering': '',
        'price_promo__gte': '',
        'price_promo__lte': '',
        'categories': '',
        'search': '',
    }

    async with aiohttp.ClientSession() as session:

        response = await session.get('https://5ka.ru/api/v2/special_offers/', params=params, headers=headers)

        j = await response.json()


        return j

async def products_str(response):

    products_raw = response.get('results', {})


    if len(products_raw) > 0:

        for product in products_raw:

            all_prise = product.get('current_prices',  False)

            name = product.get("name", None)
            price = all_prise.get("price_promo__min", None)
            oldPrice = all_prise.get("price_reg__min", None)
            if price == None and oldPrice == None:
                sale = None
            else:
                sale = f'{round((1 - float(price) / float(oldPrice)) * 100)}%'


            if sale != None:
                async with aiofiles.open(f'pyaterochka_{current_date}.csv', 'a', encoding='utf-8', newline='') as file:
                    writer = AsyncWriter(file)

                    await writer.writerow(
                        (
                            name,
                            price,
                            oldPrice,
                            sale,
                        )
                    )

    return products_raw





async def pyaterochka_main():


    for page in range(1,100):
        res = await all_tovar_str(page)
        page_res = await products_str(res)
        if page_res == []:
            return f'pyaterochka_{current_date}.csv'



if __name__ == '__main__':
    asyncio.run(pyaterochka_main())



# Установка screen: sudo apt install screen
# Создаст новый screen: screen
# Свернуть screen: CRTL + A, после чего нажмаем D
# Что-бы посмотреть список запущенных screen: screen -ls
# Что-бы вернуться к свёрнутому screen: screen -r
# Что-бы завершить сессию/закрыть screen: exit