# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import pandas as pd

import pickle

from tree_reader import generate_tree_structure, export_to_csv

API_SERVICE = "youtube"
API_VERSION = "v3"

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def authenticate():
  
  os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
  
  client_secrets_file = "client_secret.json"

  # Get credentials and create an API client
  flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
      client_secrets_file, SCOPES)
  
  credentials = None
  
  token_file = "tocken.pickle"

  if os.path.exists(token_file):
    with open(token_file, 'rb') as token:
      credentials = pickle.load(token)

  if not credentials or not credentials.valid:
    credentials = flow.run_local_server()
    
    with open(token_file, "wb") as token:
      pickle.dump(credentials, token)
    
  return credentials 

CREDENTIALS = authenticate()

CLIENT = googleapiclient.discovery.build(
      API_SERVICE, 
      API_VERSION, 
      credentials=CREDENTIALS
    )

def get_playlist_ids():
  
  request = CLIENT.playlists().list(
      part="id, snippet",
      mine=True
  )
  response = request.execute()
  
  playlists = response.get("items")
  playlist_ids = [playlist["id"] for playlist in playlists]
  playlist_names = [playlist["snippet"]["title"] for playlist in playlists]
  
  return playlist_names, playlist_ids

def get_videos(playlist_id): 
  request = CLIENT.playlistItems().list(
    part="snippet",
    playlistId=playlist_id
  )
  response = request.execute()
  
  videos = response.get("items", [])
  
  return videos

def set_tree(playlist_names, playlist_ids):
  playlist_dict = {}
  
  for i in range(len(playlist_names)):
    videos = get_videos(playlist_ids[i])
    
    video_titles = [video["snippet"]["title"] for video in videos]
    playlist_dict[playlist_names[i]] = {
      "videos": video_titles,
    }
    
  return playlist_dict
  
def main():
  playlist_names, playlist_ids = get_playlist_ids()
  
  playlist_dict = set_tree(playlist_names, playlist_ids)
  
  playlist_dict['Example1'] = {
    "videos": ["Video1.mp3", "Video2.wav"],
  }
  
  df = pd.DataFrame.from_dict(playlist_dict, orient="columns")    
    
  tree_structure = generate_tree_structure("./")
  
  df_tree = pd.DataFrame.from_dict(tree_structure, orient="columns")
  
  
  
  print(df_tree)
  
      
if __name__ == '__main__':
  main()