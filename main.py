import os
import xml.etree.ElementTree as ET

import requests

BASE_URL = 'https://cloudformation-schema.s3.us-west-2.amazonaws.com/'

try:
    response = requests.get(BASE_URL)
    root = ET.fromstring(response.content)
    namespace = "{http://s3.amazonaws.com/doc/2006-03-01/}"
    keys=[]

    for contents in root.findall(f"{namespace}Contents"):
        key = contents.find(f"{namespace}Key").text
        if key.startswith("resourcetype/"):
            keys.append(key)
    
    for key in keys:
        response = requests.get(BASE_URL+key)
        with open(key.split("/")[1], 'wb') as f:
            f.write(response.content)
except Exception as e:
    print(f'Error: {e}')
