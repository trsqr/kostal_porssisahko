import time
import requests
import json
import syslog
import urllib3
import asyncio
from pykoplenti import (ApiClient, AuthenticationException)
from aiohttp import ClientSession
urllib3.disable_warnings()

# Just change the three lines below

MARGINAL = 0.0031 # Marginal from your electricity company, note: in euros per kWh
PLENTICORE_IP = "192.168.1.3"
PLENTICORE_PASSWORD = "password"

#####

MAX = -1

async def set_power_limit(limit):
  async with ClientSession() as session:
    client = ApiClient(session, PLENTICORE_IP)
    try:
      await client.login(PLENTICORE_PASSWORD)
    except AuthenticationException as err:
      print("Authentication failed")
      exit(1)

    data_api = await client.get_setting_values({"devices:local": ['Inverter:ActivePowerLimitation', 'Inverter:MaxApparentPower']})

    device_local = data_api['devices:local']
    current_limit = device_local["Inverter:ActivePowerLimitation"]
    max_power = device_local["Inverter:MaxApparentPower"]

    if (limit == MAX):
      wanted_limit = max_power
    else:
      wanted_limit = limit

    if (current_limit == wanted_limit):
      print(f'Nothing to do, limit already set as required.')
      exit(0)

    await client.set_setting_values("devices:local", {"Inverter:ActivePowerLimitation":wanted_limit})
    print(f'OK, limit set at {wanted_limit} W.')
    exit(0)


response = requests.get('https://api.spot-hinta.fi/JustNow/')
if (response.status_code != 200):
  print("Could not get spot price, disabling power limitation!")
  asyncio.run(set_power_limit(MAX))
  exit(1)

data = response.json()
if data["PriceNoTax"] > MARGINAL:
  print(f'Price is higher than marginal ({data["PriceNoTax"]} EUR/kWh), feed in limit disabled.')
  asyncio.run(set_power_limit(MAX))
else:
  print(f'Price is too low ({data["PriceNoTax"]} EUR/kWh), limit feed in.')
  asyncio.run(set_power_limit("0"))
