import os
import re
from sclib import SoundcloudAPI
from tree_reader import generate_tree_structure

api = SoundcloudAPI()

BASE_URL = 'https://soundcloud.com/louis-calvinhac/sets/'

DATA_PATH = "./data"
TREE_STRUCTURE = generate_tree_structure(DATA_PATH)

PLAYLIST_TITLES = [
  "test",
  "acide",
  "techno"
]

def clean_title(video_title):
  cleaned = re.sub(r"[^\w\s]", "", video_title).replace(" ", "_")
  
  return cleaned

def download(path, track):
    fname = f"{clean_title(track.title)}.wav"
    with open(os.path.join(path, fname), "wb+") as f:
      track.write_mp3_to(f)
    
    tree = generate_tree_structure(DATA_PATH)
 
 
 
  
playlists = [api.resolve(BASE_URL + title) for title in PLAYLIST_TITLES]

def main():
  
  for playlist in playlists:
    print(f"Processing playlist : {playlist.title}")
    path = os.path.join(DATA_PATH, playlist.title)
    
    if not os.path.exists(path):
      
      print(f"La playlist {playlist.title} est absente de la bibliothèque locale")
      print(f"Création du répertoire /{playlist.title}...")
      os.mkdir(path)
      
      for track in playlist.tracks:
        download(path, track)
      
    else:
      for track in playlist.tracks:
        if not clean_title(track.title) in TREE_STRUCTURE[playlist.title]['videos']:
          download(path, track)
          
if __name__ == '__main__':
  main()