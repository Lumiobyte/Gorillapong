import json

filepath = "./save.json"
# Database should have a get max res function so that main menu mouse mapper isn't hardcoded

def get_max_resolution():
    with open(filepath) as file:
        data = json.load(file)
        return (data["max_resolution"][0], data["max_resolution"][1])

def get_resolution():
    with open(filepath) as file:
        data = json.load(file)
        return (data["resolution"][0], data["resolution"][1])

def set_resolution(new_res):
    with open(filepath, mode = "r") as file:
        data = json.load(file)
        
    data["resolution"] = [new_res[0], new_res[1]]

    with open(filepath, mode = "w") as file:
        json.dump(data, file)
    