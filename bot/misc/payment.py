from yoomoney import Quickpay, Client
import random
from bot.misc import EnvKeys

import asyncio
import base64
import hashlib
import json
import uuid

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ParseMode
from aiogram.dispatcher.filters import CommandStart
from bot.database.methods import buy_item, add_bought_item
from bot.keyboards import back
import datetime
from bot.logger_mesh import logger
from bot.keyboards.inline import check_payment_kb


def quick_pay(message):
    bill = Quickpay(
        receiver=EnvKeys.RECEIVER_TOKEN,
        quickpay_form="shop",
        targets="Sponsor",
        paymentType="SB",
        sum=message.text,
        label=str(message.from_user.id) + '_' + str(random.randint(1000000000, 9999999999))
    )
    label = bill.label
    url = bill.base_url
    return label, url


async def check_payment_status(label: str):
    client = Client(EnvKeys.CLIENT_TOKEN)
    history = client.operation_history(label=label)
    for operation in history.operations:
        return operation.status


async def make_request(url: str, invoice_data: dict):
    encoded_data = base64.b64encode(
        json.dumps(invoice_data).encode("utf-8")
    ).decode("utf-8")
    signature = hashlib.md5(f"{encoded_data}{'CRYPTOMUS_API_KEY'}".
                            encode("utf-8")).hexdigest()

    async with aiohttp.ClientSession(headers={
        "merchant": 'CRYPTOMUS_MERCHANT_ID',
        "sign": signature,
    }) as session:
        async with session.post(url=url, json=invoice_data) as response:
            if not response.ok:
                raise ValueError(response.reason)

            return await response.json()




async def check_invoice_paid(id: str, message, value_data, item_price, user_id, item_name):
    # while True:
    invoice_data = await make_request(
        url="https://api.cryptomus.com/v1/payment/info",
        invoice_data={"uuid": id},
    )

    if invoice_data['result']['payment_status'] in ('paid', 'paid_over'):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        buy_item(value_data['id'], value_data['is_infinity'])
        add_bought_item(value_data['item_name'], value_data['value'], item_price, user_id, formatted_time)
        await message.answer(chat_id=message.chat.id,
                             message_id=message.message_id,
                             text=f'✅ Товар куплен!',
                             reply_markup=back(f'item_{item_name}'))
        logger.info(f"Пользователь {user_id}"
                    f" купил 1 товар позиции {value_data['item_name']} за {item_price}р")
        return

    else:
        await message.answer('Оплата не прошла')
        # print("Оплата пока не прошла")

        # await asyncio.sleep(5)




async def buy_handler(message: Message, amount, value_data, item_price, user_id, item_name):
    amount = str(amount).replace(',', '.')
    invoice_data = await make_request(
        url="https://api.cryptomus.com/v1/payment",
        invoice_data={
            "amount": amount,
            "currency": "USD",
            "order_id": str(uuid.uuid4())
        },
    )
    # await asyncio.create_task(check_invoice_paid(invoice_data['result']['uuid'], message=message))
    meow = f"{invoice_data['result']['uuid']}:{value_data}:{item_price}:{user_id}:{item_name}"
    await message.answer(f"Ваш инвойс: {invoice_data['result']['url']}",
                         reply_markup=check_payment_kb(meow))
