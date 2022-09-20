import lyricsgenius
import requests
import pandas as pd
import json
import os
from bs4 import BeautifulSoup

genius = lyricsgenius.Genius('<genius_access_token>')

#will use hip-hop-fandom site to get list of Nas albums
nas_url = 'https://hip-hop-music.fandom.com/wiki/Nas'
artist = "Nas"

#Scrapes the url for albums of the artist
def get_albums(artist=artist, URL=nas_url):
    """
    
    """
    albums_page = requests.get(URL)
    html = BeautifulSoup(albums_page.content, "html.parser")
    page = html.find_all('i')
    albums = [album.get_text().strip() for album in page]
    albums = albums[7:]
    #Had to perform a manual search on album_id for album titled Untitled 
    all_albums = [genius.search_album(album_id = 76781).save_lyrics() if album == 'Untitled' else genius.search_album(album, artist).save_lyrics() for album in albums]
    return all_albums

#Makes a pandas dataframe of all albums
def create_albums_df(file_path):
    """
    
    """
    all_albums = [file for file in os.listdir(file_path) if file.endswith('.json')]
    album_dfs = []
    album_info = []
    for file_name in all_albums:
        data = json.load(open(file_name))
        for record in range(len(data['tracks'])):
            track_number = data['tracks'][record]['number']
            track_name = data['tracks'][record]['song']['title']
            album = data['name']
            release_year = data['release_date_components']['year']
            lyrics = data['tracks'][record]['song']['lyrics']
            album_info.append([track_number, track_name, album, release_year, lyrics])
    individual_df = pd.DataFrame(album_info, columns= ['track_number', 'track_name', 'album', 'release_year', 'lyrics'])
    album_dfs.append(individual_df)
    all_albums_df = pd.concat(album_dfs)
    all_albums_df.to_csv('all_albums_2.csv', index=False)
    return all_albums_df
