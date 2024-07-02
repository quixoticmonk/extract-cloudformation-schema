import json
import os

directory_path = './schema'

type_names_with_tags={}
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        file_path = os.path.join(directory_path, filename)
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Check if the "tagging" section exists and if "taggable" is true
        if 'tagging' in data and data['tagging']['taggable']:
            typename = data['typeName']
            taggable = data['tagging']['taggable']
            tags = data["properties"].get('Tags', None)
            # Check if "TagsMap" exists in "definitions"
            if "definitions" in data and "TagsMap" in data["definitions"]:
                type_names_with_tags[typename] = data["definitions"]["TagsMap"].get("type", None)            
            elif tags and tags.get('type', None) !="array" :
                if tags.get('type', None) == None:
                     if "Tags" in data["definitions"] and data["definitions"]["Tags"].get("type",None) !="array":
                        type_names_with_tags[typename] = data["definitions"]["Tags"].get("type",None)
                else:
                     type_names_with_tags[typename] = tags.get('type', None)
                     

with open('tagdetails_resources.json', 'w') as json_file:
    json.dump(type_names_with_tags, json_file, indent=2)
