import os
import re
from sclib import SoundcloudAPI
from tree_reader import generate_tree_structure

api = SoundcloudAPI()

USER = "mathieucances"
BASE_URL = f"https://soundcloud.com/{USER}/sets/"
DATA_PATH = "./data"
if not os.path.exists(DATA_PATH) : os.mkdir(DATA_PATH) 

# Module custom pour générer l'arborescence de la biibliothèque sous forme de dictionnaire
TREE_STRUCTURE = generate_tree_structure(DATA_PATH)


# Constante à modifier lors de l'ajout/suppression de playlists (insensible à la casse)
PLAYLIST_TITLES = [
  "hard techno",
  "hard core",
  "ACID",
  "rave",
  "techno",
  "trance",
  "chill",
  "gabber",
  "rock",
  "autres",
  "french core",
  "uptempo"
]
# Petite fonction pour nettoyer les titres des sons (caractères spéciaux, espaces, etc..)
def clean_title(title):
  cleaned = re.sub(r"[^\w\s]", "", title).replace(" ", "_")
  
  return cleaned

def download(path, track):
    fname = f"{clean_title(track.title)}.wav"
    try:
      with open(os.path.join(path, fname), "wb+") as f:
        track.write_mp3_to(f) 
    except:
      print(f"The track {track.title} is marked as 'Not Downloadable'")
      os.remove(os.path.join(path, fname))
        
 # Fetch toutes les playlists à partir de PLAYLIST_TITLES
playlists = [api.resolve(BASE_URL + re.sub("\s", "-", title)) for title in PLAYLIST_TITLES]

def main():
  
  # Itération sur chaque playlist récupérée
  for playlist in playlists:
    
    print(f"{'='*10} Processing playlist : {playlist.title}")
    path = os.path.join(DATA_PATH, playlist.title)
    
    # Check si le dossier {playlist_title} existe
    if not os.path.exists(path):
      
      print(f"La playlist {playlist.title} est absente de la bibliothèque locale")
      print(f"Création du répertoire /{playlist.title}...")
      os.mkdir(path)
      
      # Donwload de tous les sons de la playlist 
      for track in playlist.tracks:

        download(path, track)

    else:
      # Si le dossier est présent, check si tous les sons sont bien dans l'arborescence
      for track in playlist.tracks:
        if not clean_title(track.title) in TREE_STRUCTURE[playlist.title]['videos']:

          download(path, track)
          

            
            
            
          
          
if __name__ == '__main__':
  main()