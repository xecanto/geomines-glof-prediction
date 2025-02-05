import requests
import time
import pdb

pdb.set_trace()
username = 'abdurrehman786'
password = 'Pakistan[123]'
    
response = requests.post('https://appeears.earthdatacloud.nasa.gov/api/login',
                         auth=(username, password)
                         )
token = response.json()['token']

# Define the API endpoint for submitting a new area request
submit_url = 'https://appeears.earthdatacloud.nasa.gov/api/task'

# Define the request parameters
request_params = {
    'task_type': 'area',
    'task_name': 'Sentinel-2 Bands 1-5 Download',
    'params': {
        'layers': [
            {'product': 'S2A_SR', 'layer': 'B01'},
            {'product': 'S2A_SR', 'layer': 'B02'},
            {'product': 'S2A_SR', 'layer': 'B03'},
            {'product': 'S2A_SR', 'layer': 'B04'},
            {'product': 'S2A_SR', 'layer': 'B05'}
        ],
        'output': {
            'format': {'type': 'geotiff'},
            'projection': 'geographic'
        },
        'geo': {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [72.5127712940002, 34.51583249],
        [77.8339670880002, 34.51583249],
        [77.8339670880002, 37.0890936052039],
        [72.5127712940002, 37.0890936052039],
        [72.5127712940002, 34.51583249]
                            ]
                        ]
                    },
                    'properties': {}
                }
            ]
        },
        'dates': [
            # {'startDate': 'YYYY-MM-DD', 'endDate': 'YYYY-MM-DD'}
            # {'startDate': '2022-06-11', 'endDate': '2022-06-22'}
            # start date and end date should be in the format of 'MM-DD-YYYY'
            {'startDate': '06-11-2022', 'endDate': '06-22-2022'}
        ]
    }
}

# Submit the area request
response = requests.post(submit_url, json=request_params, headers={'Authorization': f'Bearer {token}'})
response_json = response.json()


# Check if the request was successful
if response.status_code == 200:
    task_id = response_json['task_id']
    print(f'Request submitted successfully. Task ID: {task_id}')
else:
    print(f'Error submitting request: {response_json}')
    exit()
    
# write the task_id to a file for later use
with open('task_id.txt', 'w') as file:
    file.write(task_id)

# Define the API endpoint for checking the task status
status_url = f'https://appeears.earthdatacloud.nasa.gov/api/task/{task_id}'

# Poll the task status until it is 'done'
# while True:
#     status_response = requests.get(status_url, headers={'Authorization': f'Bearer {token}'})
#     status_json = status_response.json()
#     if status_json['status'] == 'done':
#         print('Task completed successfully.')
#         break
#     elif status_json['status'] == 'error':
#         print('Error processing task.')
#         exit()
#     else:
#         print('Task is still processing. Checking again in 30 seconds...')
#         time.sleep(30)

# # Define the API endpoint for downloading the output
# bundle_url = f'https://appeears.earthdatacloud.nasa.gov/api/bundle/{task_id}'

# # Get the bundle information
# bundle_response = requests.get(bundle_url, headers={'Authorization': f'Bearer {token}'})
# bundle_json = bundle_response.json()

# # Download each file in the bundle
# for file_info in bundle_json['files']:
#     file_id = file_info['file_id']
#     file_name = file_info['file_name']
#     download_url = f'https://appeears.earthdatacloud.nasa.gov/api/bundle/{task_id}/{file_id}'
#     file_response = requests.get(download_url, headers={'Authorization': f'Bearer {token}'}, stream=True)
#     with open(file_name, 'wb') as file:
#         for chunk in file_response.iter_content(chunk_size=8192):
#             file.write(chunk)
#     print(f'Downloaded {file_name}')
