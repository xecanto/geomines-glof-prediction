import requests
import json

# Replace with your actual credentials
client_id = "sh-35d2b511-a739-46dd-82e0-6c8216e724f8"
client_secret = "rJXRWpJp9hftdZyjmyTvJi76ZwA2ahBW"
username = 'abdurrehmangoheer786@gmail.com'
password = ':rPzz9_38MCZcNv'

# Authentication URL
auth_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'

# OData API URL
odata_url = 'https://catalogue.dataspace.copernicus.eu/odata/v1/Products'

# Area of Interest (AOI) coordinates
aoi = {
    "type": "Polygon",
    "coordinates": [[
        [72.5127712940002, 34.51583249],
        [77.8339670880002, 34.51583249],
        [77.8339670880002, 37.0890936052039],
        [72.5127712940002, 37.0890936052039],
        [72.5127712940002, 34.51583249]
    ]]
}

# Function to obtain access token
# Function to obtain access token using Client Credentials Grant
def get_access_token():
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(auth_url, data=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()['access_token']


# Function to query OData API
def query_odata_api(token, start_date, end_date):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    # Constructing the filter query
    filter_query = (
        f"Collection/Name eq 'SENTINEL-2' and "
        f"ContentDate/Start ge {start_date} and "
        f"ContentDate/End le {end_date}"
        # f"OData.CSC.Intersects(area=geography'SRID=4326;"
        # f"POLYGON(({aoi['coordinates'][0][0][0]} {aoi['coordinates'][0][0][1]},"
        # f"{aoi['coordinates'][0][1][0]} {aoi['coordinates'][0][1][1]},"
        # f"{aoi['coordinates'][0][2][0]} {aoi['coordinates'][0][2][1]},"
        # f"{aoi['coordinates'][0][3][0]} {aoi['coordinates'][0][3][1]},"
        # f"{aoi['coordinates'][0][0][0]} {aoi['coordinates'][0][0][1]}))')"
    )
    params = {
        '$filter': filter_query,
        '$top': 10  # Adjust as needed
    }
    response = requests.get(odata_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Main function
def main():
    token = get_access_token()
    start_date = '2023-01-01T00:00:00.000Z'  # Adjust as needed
    end_date = '2023-12-31T23:59:59.999Z'    # Adjust as needed
    results = query_odata_api(token, start_date, end_date)
    print(f"Found {len(results['value'])} products.")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
