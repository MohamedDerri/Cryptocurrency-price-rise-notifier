import requests
from requests import exceptions
import key
import pandas as pd
from time import sleep

def get_crypto_rates(base_currency='EUR', assets='BTC,ETH,XRP,SAI'):
	url= 'https://api.nomics.com/v1/currencies/ticker'

	payload = {'key': key.NOMICS_API_KEY, 'convert': base_currency, 'ids': assets, 'interval': '1d'}
	response = requests.get(url, params=payload)
	data = response.json()

	crypto_currency, crypto_price, crypto_timestamp = [], [], []

	# print(data)
	for asset in data:
		crypto_currency.append(asset['currency'])
		crypto_price.append(asset['price'])
		crypto_timestamp.append(asset['price_timestamp'])

	raw_data = {
		'assets' : crypto_currency,
		'rates' : crypto_price,
		'timestamp' : crypto_timestamp
	}

	df = pd.DataFrame(raw_data)
	# print(df)
	return(df)

# get_crypto_rates('USD', 'SAITAMA ')

def notify_me(df, asset):
	crypto_value = float(df[df['assets'] == asset]['rates'].item())

	info = f'{asset} : {crypto_value}, Goal => {crypto_value * 10}'

	raise_delta = crypto_value
	valueTimesTen = crypto_value * 10

	if crypto_value > raise_delta:
		print(info + '\033[1;32m THE VALUE HAS BEEN RISED' + '\033[0m')
	elif crypto_value >= valueTimesTen:
		print(info + '\033[1;32m THE VALUe HAS BEEN MULTIPLIED BY TEN' + '\033[0m')
	else:
		print('\033[0;36m' + info + '\033[1;31m TARGET HAS NOT BEEN REACHED YET ' + '\033[0m')

i = 0
while True:
	print(f'=======================================({i})========================================')


	try:
		df = get_crypto_rates()

		notify_me(df, 'BTC')
		notify_me(df, 'ETH')
		notify_me(df, 'XRP')
		notify_me(df, 'SAI')
	except Exception as e:
		print('problem with retrieving data ... Retrying in few seconds.')
	i += 1
	sleep(10)

