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

import aiohttp
import asyncio
import async_timeout
import xmltodict
import dateutil.parser


class TelegramBot:
    def __init__(self, token):
        self.token = token

    @staticmethod
    async def post(session, url, params):
        async with async_timeout.timeout(10):
            async with session.post(url, json=params) as response:
                return await response.json()

    async def send(self, chat_id, message):
        params = {
            'chat_id': chat_id,
            'text': message,
        }
        url = 'https://api.telegram.org/bot%s/sendMessage' % self.token
        async with aiohttp.ClientSession() as session:
            resp = await TelegramBot.post(session, url, params)
