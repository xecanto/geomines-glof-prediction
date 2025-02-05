import requests

username = 'abdurrehman786'
password = 'Pakistan[123]'
    
response = requests.post('https://appeears.earthdatacloud.nasa.gov/api/login',
                         auth=(username, password)
                         )
token_response = response.json()
print(token_response)