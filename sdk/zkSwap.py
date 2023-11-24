import asyncio
from loguru import logger
import aiohttp
from sdk.excel import Excel
from Data.CONSTANT import *

async def get_response(response):
    return await response.json()

async def reqst(address: str, number: int):

    async with aiohttp.ClientSession() as session:
        try:
            totalReward = 0

            response = await session.get(url_1 + address)
            token_1 = await get_response(response)
            if token_1:
                totalReward += int(token_1['amount'])

            response = await session.get(url_2 + address)
            token_2 = await get_response(response)
            if token_2:
                totalReward += int(token_2['amount'])

            response = await session.get(url_3 + address)
            token_3 = await get_response(response)
            if token_3:
                totalReward += int(token_3['amount'])

            response = await session.get(url_4 + address)
            token_4 = await (get_response(response))
            if token_4:
                totalReward += int(token_4['amount'])

            Excel.sheet[f'A{number+1}'] = address
            if totalReward != 0:
                Excel.sheet[f'B{number+1}'] = totalReward // 10**18
            else:
                Excel.sheet[f'B{number+1}'] = 0

        except Exception as e:
            logger.error(f'Ошибка: {e}')

async def get_eligible(wallets: list):

    tasks = []
    logger.info(f'Найдено {len(wallets)} кошельков')
    for address in wallets:
        tasks.append(asyncio.create_task(reqst(address, wallets.index(address)+1)))

    await asyncio.gather(*tasks)

def main_check(wallets: list):
    Excel()

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(get_eligible(wallets))
        loop.close()

    except:
        logger.error('Проблема с указанием кошелька(ов)')


    Excel.workbook.save('results/result.xlsx')