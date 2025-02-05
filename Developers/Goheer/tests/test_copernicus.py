import requests

# Replace with your client_id and client_secret
client_id = "sh-35d2b511-a739-46dd-82e0-6c8216e724f8"
client_secret = "rJXRWpJp9hftdZyjmyTvJi76ZwA2ahBW"

# Obtain access token
def get_access_token(client_id, client_secret):
    auth_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(auth_url, data=auth_data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Failed to obtain access token: {response.status_code}, {response.text}")
        return None

# Search for Sentinel-2 products
def search_sentinel2_data(token, cloud_cover, product_type, start_date, end_date, max_records):
    search_url = "https://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "cloudCover": cloud_cover,  # Cloud cover percentage range
        "productType": product_type,  # Product type (e.g., S2MSI2A)
        "startDate": start_date,  # Start date
        "completionDate": end_date,  # End date
        "maxRecords": max_records,  # Maximum number of records
    }

    response = requests.get(search_url, headers=headers, params=params)
    
    print("Request URL:", response.url)  # Debugging: print constructed URL

    if response.status_code == 200:
        return response.json().get("features", [])
    else:
        print(f"Failed to search data: {response.status_code}, {response.text}")
        return []

# Main program
if __name__ == "__main__":
    token = get_access_token(client_id, client_secret)
    if not token:
        exit()

    # Define search parameters
    cloud_cover = "[0,10]"  # Cloud cover percentage range
    product_type = "S2MSI2A"  # Sentinel-2 product type
    start_date = "2022-06-11"
    end_date = "2022-06-22"
    max_records = 10

    # Search for products
    results = search_sentinel2_data(token, cloud_cover, product_type, start_date, end_date, max_records)

    # Display results
    if results:
        print(f"{len(results)} products found.")
        for product in results:
            product_id = product["properties"]["id"]
            date = product["properties"]["startDate"]
            print(f"ID: {product_id}, Date: {date}")
    else:
        print("No products found.")



# Download a selected product

# product_id = "your_selected_product_id"  # Replace with a product ID from the search results
# product_id = "S2B_MSIL1C_20230101T051959_N0302_R119_T42TVM_20230101T073059"
# download_url = f"https://sh.dataspace.copernicus.eu/api/v1/products/{product_id}/downloads"
# response = requests.get(download_url, headers=headers)

# if response.status_code == 200:
#     with open(f"{product_id}.zip", "wb") as f:
#         f.write(response.content)
#     print(f"Product {product_id} downloaded successfully.")
# else:
#     print(f"Failed to download product: {response.status_code}, {response.text}")
