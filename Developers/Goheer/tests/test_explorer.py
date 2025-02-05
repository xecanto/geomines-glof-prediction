from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer

api = API("username", "password")
scenes = api.search(
    dataset="LANDSAT_8_C1",
    bbox=[x_min, y_min, x_max, y_max],
    max_cloud_cover=10
)
print(f"{len(scenes)} scenes found.")

ee = EarthExplorer("username", "password")
ee.download(scene_id="LANDSAT_8_C1_scene_id", output_dir="data/")
ee.logout()