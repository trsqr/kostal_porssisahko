import time
import requests
import json
import syslog
import urllib3
import asyncio
from pykoplenti import (ApiClient, AuthenticationException)
from aiohttp import ClientSession
urllib3.disable_warnings()

# Change only the 3 lines below:

MARGINAL = 0.0031 # How much is the marginal that your electricity company takes
PLENTICORE_IP = "192.168.1.3" # Inverter IP Address
PLENTICORE_PASSWORD = "inverter_password"

###################

MAX = -1

def check_http(resp):
  if (resp.status_code > 299):
    print(f'KSEM request failed. Response: {resp.status_code}')
    exit(2)

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

    print(f"Active Power Limitation: {current_limit} / {max_power}\n")

    if (limit == MAX):
      wanted_limit = max_power
    else:
      wanted_limit = limit

    if (current_limit == wanted_limit):
      print(f'Nothing to do, limit already set as required.')
      exit(0)

    await client.set_setting_values("devices:local", {"Inverter:ActivePowerLimitation":wanted_limit})

    print(f'OK')
    exit(0)


  headers = {"Authorization": f'Bearer {KSEM_TOKEN}'}
  response = requests.get(f'https://{KSEM_IP}/api/kostal-energyflow/configuration', headers = headers, verify = False)
  check_http(response)

  ksem_data = response.json()

  if (limit == 0):
    print("Disabling grid feed in.")
    if (ksem_data["powerreduction"]["limit"] == 0):
      print(f'Nothing to do, limit at 0 already.')
    else:
      print(f'Changing limit from {ksem_data["powerreduction"]["limit"]} to 0.')
      ksem_data["powerreduction"]["limit"] = 0
      ksem_data["powerreduction"]["enabled"] = True
      ksem_data_str=json.dumps(ksem_data)
      response = requests.put(f'https://{KSEM_IP}/api/kostal-energyflow/configuration', headers = headers, data = ksem_data_str.lower(), verify = False)
      check_http(response)

      response = requests.get(f'https://{KSEM_IP}/api/kostal-energyflow/configuration', headers = headers, verify = False)
      check_http(response)
      ksem_data = response.json()
      if (ksem_data["powerreduction"]["limit"] == 0):
        print("Operation verified.")
        syslog.syslog("Grid feed in disabled due to low electricity price.")

  elif (limit == MAX):
    if (ksem_data["powerreduction"]["limit"] == ksem_data["powerreduction"]["maxpower"]):
      print(f'Nothing to do, limit at {ksem_data["powerreduction"]["limit"]} (MAX) already.')
    else:
      print(f'Changing limit from {ksem_data["powerreduction"]["limit"]} to {ksem_data["powerreduction"]["maxpower"]} (MAX).')
      ksem_data["powerreduction"]["limit"] = ksem_data["powerreduction"]["maxpower"]
      ksem_data_str=json.dumps(ksem_data)
      print(ksem_data_str.lower())
      response = requests.put(f'https://{KSEM_IP}/api/kostal-energyflow/configuration', headers = headers, data = ksem_data_str.lower(), verify = False)
      check_http(response)

      response = requests.get(f'https://{KSEM_IP}/api/kostal-energyflow/configuration', headers = headers, verify = False)
      check_http(response)
      ksem_data = response.json()
      if (ksem_data["powerreduction"]["limit"] == ksem_data["powerreduction"]["maxpower"]):
        print("Operation verified.")
        syslog.syslog("Grid feed in activated.")

  else:
    print("Something else.")

time.sleep(3)
response = requests.get('https://api.spot-hinta.fi/JustNow/')
if (response.status_code != 200):
  print("Could not get spot price, disabling power limitation!")
  set_power_limit(MAX)
  exit(1)

data = response.json()
if data["PriceNoTax"] > MARGINAL:
  print(f'Price is higher than marginal ({data["PriceNoTax"]} EUR/kWh), disabling feed in limit.')
  asyncio.run(set_power_limit(MAX))
else:
  print(f'Price is too low ({data["PriceNoTax"]} EUR/kWh), limit feed in.')
  print(data["PriceNoTax"])
  asyncio.run(set_power_limit(0))
