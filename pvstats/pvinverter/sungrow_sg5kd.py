#!/usr/bin/env python

# Copyright 2018 Paul Archer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from decimal import *
from time import sleep

from pymodbus.client.sync import ModbusSerialClient
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from pymodbus.transaction import ModbusSocketFramer

from pvstats.pvinverter.base import BasePVInverter
from pvstats.pvinverter.sungrow_sg5ktl import PVInverter_SunGrow

getcontext().prec = 9

import logging

_logger = logging.getLogger(__name__)

_register_map = {
    'input': {
        '5003': {'name': 'daily_pv_power', 'scale': Decimal(100), 'units': 'W'},
        '5004': {'name': 'lifetime_pv_power', 'scale': Decimal(1), 'units': 'kW'},
        '5008': {'name': 'internal_temp', 'scale': Decimal('0.1'), 'units': 'C'},
        '5011': {'name': 'pv1_voltage', 'scale': Decimal('0.1'), 'units': 'V'},
        '5012': {'name': 'pv1_current', 'scale': Decimal('0.1'), 'units': 'A'},
        '5013': {'name': 'pv2_voltage', 'scale': Decimal('0.1'), 'units': 'V'},
        '5014': {'name': 'pv2_current', 'scale': Decimal('0.1'), 'units': 'A'},
        '5017': {'name': 'total_pv_power', 'scale': Decimal(1), 'units': 'W'},
        '5019': {'name': 'grid_voltage', 'scale': Decimal('0.1'), 'units': 'V'},
        '5022': {'name': 'inverter_current', 'scale': Decimal('0.1'), 'units': 'A'},
        '5031': {'name': 'inverter_ac_output', 'scale': Decimal(1), 'units': 'W', 'type': 'int16'},
        '5036': {'name': 'grid_frequency', 'scale': Decimal('0.1'), 'units': 'Hz'},
    },

    'holding': {
        '5000': {'name': 'date_year', 'scale': 1, 'units': 'year'},
        '5001': {'name': 'date_month', 'scale': 1, 'units': 'month'},
        '5002': {'name': 'date_day', 'scale': 1, 'units': 'day'},
        '5003': {'name': 'date_hour', 'scale': 1, 'units': 'hour'},
        '5004': {'name': 'date_minute', 'scale': 1, 'units': 'minute'},
        '5005': {'name': 'date_second', 'scale': 1, 'units': 'second'},
    }
}


class PVInverter_SunGrow_SG5KD(PVInverter_SunGrow):
    def __init__(self, cfg, **kwargs):
        super(PVInverter_SunGrow, self).__init__()
        self.cfg = cfg
        self.client = ModbusTcpClient(self.cfg['host'], port=self.cfg['port'],
                                    framer=ModbusSocketFramer, timeout=5,
                                    RetryOnEmpty=True, retries=5)

__all__ = [
    "PVInverter_SunGrow_SG5KD"
]

# vim: set expandtab ts=2 sw=2:
