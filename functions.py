import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any

import aiohttp
from aiogram.types import Message
from loguru import logger

CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"


class Clients:
    def __init__(self):
        self.dict = {}

    async def set_clients(self, data: dict):
        try:
            self.dict[f"{data['id']}"] = {"username": data['username'], "name": data['name'],
                                          "reasons": data["reasons"], "date": data["date"]}
        except Exception as e:
            logger.exception('Исключение вызванное functions/set_clients', e)

    async def update_clients(self, id: str, key: str, value: str):
        try:
            self.dict[id][key] = value
        except Exception as e:
            logger.exception('Исключение вызванное functions/update_clients', e)

    async def get_clients(self) -> dict:
        return self.dict

    async def load_base(self, clients_list: list):
        try:
            for i in clients_list:
                data = {"id": i[0],"username": i[1], "name": i[2],
                        "reasons": i[3], "date": i[4]}
                await self.set_clients(data)
        except Exception as e:
            logger.exception('Исключение вызванное functions/load_base', e)



clients_base = Clients()


async def is_today(date_str: str) -> bool:
    try:
        input_date = datetime.strptime(date_str, "%d.%m.%y %H:%M")
        now = datetime.now()
        return input_date.date() == now.date()
    except ValueError:
        return False  # если строка не распарсилась


# напиши функцию для вычисления факториала

# asyncio.run(clients_base.load_base(asyncio.run(Sheet_base(None, None).get_clients())))
# # print(asyncio.run(clients_base.get_clients()))
#
# for i in asyncio.run(clients_base.get_clients()).values():
#     print(asyncio.run(is_today(i["date"])))

