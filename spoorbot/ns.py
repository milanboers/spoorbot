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
import async_timeout
import xmltodict
import dateutil.parser
import datetime
from collections import namedtuple


class TravelPossibility(namedtuple('TravelPossibility', ['leave_time_planned', 'leave_time_real', 'arrival_time_planned', 'arrival_time_real'])):
    @property
    def leave_delay_mins(self):
        return (self.leave_time_real - self.leave_time_planned).total_seconds() / 60

    @property
    def arrive_delay_mins(self):
        return (self.arrival_time_real - self.arrival_time_planned).total_seconds() / 60

    @property
    def pretty_printed(self):
        leave_delay = self.leave_delay_mins
        arrive_delay = self.arrive_delay_mins
        leave_suffix = '+' + str(round(leave_delay)) if leave_delay != 0 else ''
        arrive_suffix = '+' + str(round(arrive_delay)) if arrive_delay != 0 else ''
        duration = str(round((self.arrival_time_real - self.leave_time_real).total_seconds() / 60))
        return self.leave_time_planned.strftime('%H:%M') + leave_suffix\
            + ' - '\
            + self.arrival_time_planned.strftime('%H:%M') + arrive_suffix\
            + ' (' + duration + ' mins)'


class NSApi:
    def __init__(self, login, password):
        self.auth = aiohttp.BasicAuth(login, password)

    @staticmethod
    async def fetch(session, url, params):
        async with async_timeout.timeout(10):
            async with session.get(url, params=params) as response:
                return await response.text()

    async def plan(self, from_station, to_station):
        params = {
            'fromStation': from_station,
            'toStation': to_station,
            'previousAdvices': 0,
            'nextAdvices': 5,
        }
        url = 'https://webservices.ns.nl/ns-api-treinplanner'
        async with aiohttp.ClientSession(auth=self.auth) as session:
            xml = await NSApi.fetch(session, url, params)
            parsed = xmltodict.parse(xml)
            possibilities = map(
                lambda x: TravelPossibility(
                    dateutil.parser.parse(x['GeplandeVertrekTijd']),
                    dateutil.parser.parse(x['ActueleVertrekTijd']),
                    dateutil.parser.parse(x['GeplandeAankomstTijd']),
                    dateutil.parser.parse(x['ActueleAankomstTijd']),
                ),
                parsed['ReisMogelijkheden']['ReisMogelijkheid'])
            return list(possibilities)
