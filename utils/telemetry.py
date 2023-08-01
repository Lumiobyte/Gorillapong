import time
import requests
import threading
import platform
import psutil
from utils import database
from pygame.locals import FULLSCREEN
from pygame.display import Info

class TelemetryModule:

    def __init__(self):
        """ Setup strings """

        self.root_domain = 'https://zirconium.lumiobyte.net/api/log/'

        self.system_hostname = self.check_empty(platform.node())

    def check_empty(self, string):
        """ Ensure that the resultant string is not empty """
        if string is None or string == "":
            return "Unknown"
        else:
            return string

    def sysinfo(self):
        """ Post system information to API """

        display_info = Info()

        data = {"hostname": self.system_hostname, "os": platform.platform(), "processor": self.check_empty(platform.processor()), "pyver": platform.python_version(), "screenres": f"{display_info.current_w}x{display_info.current_h}", "physicalmem": psutil.virtual_memory().total}
        threading.Thread(target = self.make_request, args = ("sysinfo", data,), daemon = True).start()

    def gamesettings(self):
        """ Post game setting configuration to API """

        music_sound_toggles = database.get_music_sound()
        music_sound_volumes = database.get_volume()

        gameplay_settings = database.get_all_gameplay_settings(False)
        gameplay_settings[7] = 1 if gameplay_settings[7] is True else 0
        gameplay_settings_str = ""
        for item in gameplay_settings:
            gameplay_settings_str += f"{str(item)},"

        gameplay_settings_str = gameplay_settings_str.rstrip(",")

        res = database.get_resolution()
        if res == FULLSCREEN:
            res = "0"
        else:
            res = f"{res[0]}x{res[1]}"

        data = {"hostname": self.system_hostname, "res": res, "mtog": music_sound_toggles[0], "stog": music_sound_toggles[1], "mvol": music_sound_volumes[0], "svol": music_sound_volumes[1], "gset": gameplay_settings_str}
        threading.Thread(target = self.make_request, args = ("gamesettings", data,), daemon = True).start()

    def click(self, action_id):
        """ Post a click event to API """

        print("Log click: " + str(action_id))

        data = {"hostname": self.system_hostname, "time": time.time(), "action": action_id}
        threading.Thread(target = self.make_request, args = ("click", data,), daemon = True).start()

    def session(self, type, mode, time_elapsed, score1, score2, bounces, misses):
        """ Post a game session event to API """

        data = {"hostname": self.system_hostname, "time": time.time(), "setype": type, "mode": mode, "elapsed": time_elapsed.total_seconds(), "s1": score1, "s2": score2, "bounces": bounces, "misses": misses}
        threading.Thread(target = self.make_request, args = ("session", data,), daemon = True).start()

    def error(self, error_name, error_string):
        """ Post an error event to API """

        data = {"hostname": self.system_hostname, "time": time.time(), "err_name": self.check_empty(error_name), "err": self.check_empty(error_string)}
        threading.Thread(target = self.make_request, args = ("error", data,), daemon = True).start()

    def make_request(self, ext, data):
        """ This function will be called as a daemon thread to prevent blocking the main loop """

        try:
            response = requests.post(self.root_domain + ext, json = data)
            print(response.status_code)
        except requests.exceptions.ConnectionError:
            print(f"TM: Connection error when posting {ext} log\nPLEASE RUN THE GAME WITH AN INTERNET CONNECTION!")
            # DEAR Ms Blansjaar or Mr Chadwick
            # I have spent upwards of 10 hours building this telemetry system and its accompanying Django site.
            # Running the game without an internet connection would be a crime.
            # I will SHOW YOU what I logged if you come and ask me.
            # No ulterior motive. I just want to see what buttons you click!
            # I only take your system hostname to identify requests coming from your computer, and not mine/somebody else's!