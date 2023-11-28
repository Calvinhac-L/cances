import os
import pickle

# Import des librairies d'authentication API Youtube
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


# Custom module pour lire l'arborescence de la bibliothèque
from tree_reader import generate_tree_structure

# Module pyTube pour simplifier le DL (A migrer complètement si entretenu)
from pytube import YouTube

# Module de RegEx pour la comparaison de noms de fichiers
import re

API_SERVICE = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

# Chemin source de la bibliothèque
LOCAL_PATH = "./songs"

# Lecture de la bibliothèque + On stocke le nom des playlists locales dans une liste
tree_structure = generate_tree_structure(LOCAL_PATH)
local_playlists = [*tree_structure.keys()]


# Fonction d'authentification à l'API Youtube (A virer si jamais pyTube suffisant)
def authenticate():
  
  os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
  
  client_secrets_file = "client_secret.json"

  flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
      client_secrets_file, SCOPES)
  
  credentials = None
  
  
  # Enregistrement du token d'authentification  
  token_file = "token.pickle"

  if os.path.exists(token_file):
    with open(token_file, 'rb') as token:
      credentials = pickle.load(token)

  if not credentials or not credentials.valid:
    credentials = flow.run_local_server()
    
    with open(token_file, "wb") as token:
      pickle.dump(credentials, token)
    
  return credentials 

CREDENTIALS = authenticate()

# Création du client API
CLIENT = googleapiclient.discovery.build(
      API_SERVICE, 
      API_VERSION, 
      credentials=CREDENTIALS
    )

# On requête l'API Youtube pour obtenir toutes les playlists enregistrées
def get_playlists():
  
  request = CLIENT.playlists().list(
      part="id, snippet",
      mine=True
  )
  response = request.execute()
  
  playlists = response.get("items")
  playlist_ids = [playlist["id"] for playlist in playlists]
  playlist_names = [playlist["snippet"]["title"] for playlist in playlists]
  
  return playlist_names, playlist_ids


# On requête l'API Youtube pour obtenir les infos des vidéos dans une playlist
def get_videos(playlist_id): 
  
  # TODO : Add a download of the video as a .wav file at the end.
  request = CLIENT.playlistItems().list(
    part="snippet",
    playlistId=playlist_id
  )
  response = request.execute()
  
  videos = response.get("items", [])
  
  return videos


# Nettoyage du titres des vidéos pour le DL et l'enregistrement
def clean_title(video_title):
  cleaned = re.sub(r"[^\w\s]", "", video_title).replace(" ", "_")
  
  return cleaned

def download_video(playlist_name, video_name, video_id):
  print(f"Downloading missing video from [{playlist_name}] : {video_name}...")
  url = f"youtube.com/watch?v={video_id}"
  yt = YouTube(url)
  filter = yt.streams.filter(only_audio=True, adaptive=True).first()
          
  filter.download(output_path=os.path.join(LOCAL_PATH, playlist_name), filename=f"{video_name}.mp4")

def check_local_playlist(playlist_name, video_names, video_ids, tree_structure):
  tree_structure = generate_tree_structure(LOCAL_PATH)
  local_playlists = [*tree_structure.keys()]
  for video_name, video_id in zip(video_names, video_ids):

    if playlist_name in local_playlists and video_name not in tree_structure[playlist_name]['videos']:
      download_video(playlist_name, video_name, video_id)
        
    elif playlist_name not in local_playlists:
      print(f"La playlist : {playlist_name} ne fait pas partie de la bibliothèque locale.")
      
      os.makedirs(os.path.join(LOCAL_PATH, playlist_name))
      
      print(f"Téléchargement de la playlist {playlist_name}...")
      
      download_video(playlist_name, video_name, video_id)
      

def comparison(playlist_names, playlist_ids):
    
  for playlist_name, playlist_id in zip(playlist_names, playlist_ids):
    videos = get_videos(playlist_id=playlist_id)
    video_ids = [video['snippet']['resourceId']['videoId'] for video in videos]
    video_names = [clean_title(video['snippet']['title']) for video in videos]
    
    check_local_playlist(playlist_name, video_names, video_ids, tree_structure)
  
def main():
  playlist_names, playlist_ids = get_playlists()
  
  comparison(playlist_names, playlist_ids)

  
      
if __name__ == '__main__':
  main()