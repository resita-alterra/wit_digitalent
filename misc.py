import os
cwd = os.getcwd()
asset_path = cwd+"/asset"
fruit_subpath = "/fruits"
sweets_subpath = "/sweets"
# iterate through all file

def get_all_file_in_subpath(subpath):
    files = []
    path = asset_path + subpath
    for file in os.listdir(path):
        # Check whether file is in text format or not
        if file.endswith(".png"):
            files.append(f"{path}/{file}")
    return files

def get_all_fruits():
    return get_all_file_in_subpath(fruit_subpath)

def get_all_sweets():
    return get_all_file_in_subpath(sweets_subpath)
    