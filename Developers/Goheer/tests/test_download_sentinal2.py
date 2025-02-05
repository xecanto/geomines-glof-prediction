# from sentinelhub import SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, MimeType

# config = SHConfig()
# config.sh_client_id = ''
# config.sh_client_secret = ''

# # Define the bounding box of the shapefile
# bounding_box = BBox(bbox=[x_min, y_min, x_max, y_max], crs=CRS.WGS84)

# # SentinelHub Request
# request = SentinelHubRequest(
#     data_folder='tests/output_download_sentinel2',
#     evalscript='''
#     // Use an evalscript to calculate NDWI or other indices    
#     ''',
#     # evalscript='''
#     # NDWI = (B03 - B08) / (B03 + B08);
#     # return [NDWI];
#     # ''',    
#     input_data=[SentinelHubRequest.input_data(data_collection=DataCollection.SENTINEL2_L1C)],
#     bbox=bounding_box,
#     resolution=(10, 10),
#     responses=[
#         SentinelHubRequest.output_response('default', MimeType.TIFF)
#     ],
# )
# request.save_data()

from sentinelhub import SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, MimeType

# Initialize Sentinel Hub configuration
config = SHConfig()
config.sh_client_id = 'sh-35d2b511-a739-46dd-82e0-6c8216e724f8'
config.sh_client_secret = 'rJXRWpJp9hftdZyjmyTvJi76ZwA2ahBW'

# Define bounding box for the area of interest (replace with actual coordinates)
x_min = 72.5127712940002
y_min = 34.51583249
x_max = 77.8339670880002
y_max = 37.0890936052039
bounding_box = BBox(bbox=[x_min, y_min, x_max, y_max], crs=CRS.WGS84)

# Evalscript to calculate NDWI
evalscript = """
//VERSION=3
function setup() {
    return {
        input: ["B03", "B08"],
        output: { bands: 1 }
    };
}

function evaluatePixel(sample) {
    let ndwi = (sample.B03 - sample.B08) / (sample.B03 + sample.B08);
    return [ndwi];
}
"""

# Define Sentinel Hub request
request = SentinelHubRequest(
    data_folder="tests/output_download_sentinel2",
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,  # Level-1C Sentinel-2 data
            time_interval=("2023-01-01", "2023-12-31")  # Date range
        )
    ],
    bbox=bounding_box,
    size=(512, 512),  # Resolution in pixels
    config=config,
    responses=[
        SentinelHubRequest.output_response("default", MimeType.TIFF)
    ]
)

# Download and save data
# response = request.get_data(save_data=True, data_folder="tests/output_download_sentinel2")
request.save_data()

print("Download complete. NDWI raster saved to 'tests/output_download_sentinel2'.")

