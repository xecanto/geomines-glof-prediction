import requests
import json

# params = {
#     # 'pretty': True,
# }

# product_id = 'SRTMGL1_NC.003'

# response = requests.get(
#     f"https://appeears.earthdatacloud.nasa.gov/api/product/{product_id}",
#     params=params
# )
# product_response = response.json()
# print(json.dumps(product_response, indent=2))

token = '93lwTJ4HIM92el4kQ6MNqFtE47QSf2603XyYBbdow3B4ytHT3-HqPsO7Pp8s5_MfvdnOKRgUYMFmV8VKvw9liw'

products_url = "https://appeears.earthdatacloud.nasa.gov/api/product"
response = requests.get(products_url, headers={'Authorization': f'Bearer {token}'})

products = response.json()
print(json.dumps(products, indent=2))

