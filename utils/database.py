import json
import os 

from pygame import FULLSCREEN

filepath = os.path.abspath("./save.json")

# This dictionary maps number values stored in the database to human-readable text
gameplay_setting_text_map = {
    "casual_score_goal": None,
    "casual_ball_speed": ["Normal", "Fast"],
    "casual_powerups":  ["OFF", "Few", "Normal", "Many", "Party"],
    "casual_ai_difficulty": ["Easy", "Normal", "Hard"],
    "comp_score_goal": None,
    "comp_ball_speed": ["Normal", "Fast"],
    "comp_serve_miss_penalty": ["None", "Lose Point", "Lose Life"],
    "comp_ball_speedup": {True: "ON", False: "OFF"}
}

def get_max_resolution():
    """ Return the maximum resolution (below fullscreen) that the game can use. """
    with open(filepath) as file:
        data = json.load(file)
        return (data["max_resolution"][0], data["max_resolution"][1])

def get_resolution():
    """ Return the current resolution that the game is set to. """
    with open(filepath) as file:
        data = json.load(file)
        if data["resolution"][0] == 0:
            return FULLSCREEN 
        else:
            return (data["resolution"][0], data["resolution"][1])

def set_resolution(new_res):
    """ Set the resolution for the game to run at. Any code that calls this also prompts a restart of the game """
    with open(filepath, mode = "r") as file:
        data = json.load(file)
        
    data["resolution"] = [new_res[0], new_res[1]]

    with open(filepath, mode = "w") as file:
        json.dump(data, file)

def get_music_sound():
    """ Returns configuration variables for game music and sound effects """
    with open(filepath) as file:
        data = json.load(file)
        return (data["music"], data["sound"])
    
def toggle_music_sound(which):
    """ Toggle a configuration variable for game music and sound effects """
    with open(filepath, mode = "r") as file:
        data = json.load(file)
        
    if data[which] == True:
        data[which] = False
    else:
        data[which] = True

    with open(filepath, mode = "w") as file:
        json.dump(data, file)

    return data[which]

def get_volume():
    """ Return game music and sound effect volume settings """
    with open(filepath) as file:
        data = json.load(file)

        return (data["music_vol"], data["sound_vol"])
    
def set_volume(which, vol):
    """ Set game music or sound effects volume setting """
    with open(filepath, mode = "r") as file:
        data = json.load(file)

        data[which] = vol

    with open(filepath, mode = "w") as file:
        json.dump(data, file)

    return data[which]

def get_stats_toggle():
    """ Return configuration variable for game window stats """
    with open(filepath) as file:
        data = json.load(file)

        return data["show_stats"]
    
def toggle_stats_toggle():
    """ Toggle game window stats """
    with open(filepath, mode = "r") as file:
        data = json.load(file)

        if data["show_stats"]:
            data["show_stats"] = False
        else:
            data["show_stats"] = True

    with open(filepath, mode = "w") as file:
        json.dump(data, file)

    return data["show_stats"]

def change_gameplay_setting(setting):
    """ Iterate a gameplay setting variable to its next available option (e.g. speed: slow -> medium -> fast -> back to slow) """
    with open(filepath, mode = "r") as file:
        data = json.load(file)

        return_value = None # The updated setting is returned so it can be shown on its button to the user in the settings menu

        if setting == "casual_score_goal":
            if data[setting] < 100:
                data[setting] += 5
            else:
                data[setting] = 0

            return_value = str(data[setting]) if data[setting] > 0 else "Infinite"
        
        elif setting == "casual_ball_speed" or setting == "comp_ball_speed": # Both have the same options and can therefore be combined
            if data[setting] < 1:
                data[setting] += 1
            else:
                data[setting] = 0

            return_value = ["Normal", "Fast"][data[setting]]

        elif setting == "casual_powerups":
            if data[setting] < 4:
                data[setting] += 1
            else:
                data[setting] = 0

            return_value = ["OFF", "Few", "Normal", "Many", "Party"][data[setting]]

        elif setting == "casual_ai_difficulty":
            if data[setting] < 2:
                data[setting] += 1
            else:
                data[setting] = 0

            return_value = ["Easy", "Normal", "Hard"][data[setting]]

        elif setting == "comp_score_goal":
            if data[setting] < 30:
                data[setting] += 5
            elif data[setting] < 100:
                data[setting] += 10
            else:
                data[setting] = 10

            return_value = str(data[setting])

        elif setting == "comp_serve_miss_penalty":
            if data[setting] < 2:
                data[setting] += 1
            else:
                data[setting] = 0

            return_value = ["None", "Lose Point", "Lose Life"][data[setting]]

        elif setting == "comp_ball_speedup":
            if data[setting]:
                data[setting] = False
                return_value = "OFF"
            else:
                data[setting] = True
                return_value = "ON"

    with open(filepath, mode = "w") as file:
        json.dump(data, file)

    return return_value

def get_all_gameplay_settings(titles = True):
    """ Return the configuration of all gameplay settings in a human readable format 
        The text returned is shown on its respective button """
    with open(filepath) as file:
        data = json.load(file)

        values = []
        for setting in gameplay_setting_text_map:
            if titles:
                if gameplay_setting_text_map[setting] is None:
                    val = str(data[setting])
                    values.append(val if val != "0" else "Infinite") # When the target score is 0, there is no win condition, so show "infinite" on the button
                else:
                    values.append(gameplay_setting_text_map[setting][data[setting]])
            else:
                values.append(data[setting])

        return values
        
def get_gameplay_setting(setting):
    """ Get single gameplay config variable """
    with open(filepath) as file:
        data = json.load(file)

        return gameplay_setting_text_map[setting][data[setting]]
    
def set_stat(stat, change):
    """ Update a statistic variable """
    with open(filepath, mode = 'r') as file:
        data = json.load(file)

        data['stats'][stat] += change
        return_value = data['stats'][stat]

    with open(filepath, mode = 'w') as file:
        json.dump(data, file)

    return return_value

def get_stat(stat):
    """ Get a statistic variable """
    with open(filepath) as file:
        data = json.load(file)

        return data['stats'][stat]
    
def get_all_stats():
    """ Return dict of all statistic variables """
    with open(filepath) as file:
        data = json.load(file)

        return data['stats']
    
def reset_stats():
    """ Reset all stats """
    with open(filepath, mode = 'r') as file:
        data = json.load(file)

        data['stats'] = {"total_bounces": 0, "total_playtime": 0, "playtime_0": 0, "playtime_1": 0, "playtime_2": 0, "playtime_3": 0, "total_powerups": 0, "total_pixels_travelled": 0, "total_points_scored_p1": 0, "total_points_scored_p2": 0, "serves_missed": 0}

    with open(filepath, mode = 'w') as file:
        json.dump(data, file)
    
def get_tosaccept():
    """ Retrieve TOS accept status"""
    with open(filepath) as file:
        data = json.load(file)

        return data["tosaccept"]
    
def accept_tos(accept = True):
    """ Accept TOS (or revoke if False is passed) """
    with open(filepath, mode = 'r') as file:
        data = json.load(file)

        data["tosaccept"] = accept

    with open(filepath, mode = 'w') as file:
        json.dump(data, file)
