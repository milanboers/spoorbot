#! /usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2018, Milan Boers
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
from spoorbot import telegram, ns
import aiocron
import yaml
import os

NS_LOGIN = os.environ['NS_LOGIN']
NS_PASSWORD = os.environ['NS_PASSWORD']

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

telegram_bot = telegram.TelegramBot(TELEGRAM_TOKEN)
ns_api = ns.NSApi(NS_LOGIN, NS_PASSWORD)


async def main(frm, to):
    possibilities = await ns_api.plan(frm, to)
    prints = list(map(lambda x: x.pretty_printed, possibilities))
    prints.insert(0, '%s - %s' % (frm, to))
    await telegram_bot.send(TELEGRAM_CHAT_ID, '\n'.join(prints))


def get_journeys():
    with open('config.yml', 'r') as f:
        return yaml.load(f)['journeys']


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    journeys = get_journeys()
    for journey in journeys:
        cron = aiocron.crontab(journey['cron'], func=main, args=(journey['from'], journey['to']), loop=loop)
    loop.run_forever()
