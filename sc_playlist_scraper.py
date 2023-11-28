from sclib import SoundcloudAPI, Playlist

import re


user = "louis-calvinhac"
playlist_name = "test"
playlist = SoundcloudAPI().resolve(f"https://soundcloud.com/{user}/sets/")

print(playlist)


