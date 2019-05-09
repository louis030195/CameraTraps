import requests
import json



# #example for image upload
api_url = '<enter api url here>'
files = {'media': open('S1_F10_R1_PICT0104.JPG', 'rb')}
upload_result = requests.post(api_url, files=files).json()



#example for image url
image_http_url = '<enter image url here>'
image_url = {'image_url': image_http_url}
url_result = requests.get('http://url/v1/camera_trap_api/detect', params=image_url).json()


