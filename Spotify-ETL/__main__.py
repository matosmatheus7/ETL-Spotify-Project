# Libraries
import os
import configparser
from api_conn import APIConn
from artist import Artist
from track import Track
from album import Album
import time

def load(songs, artist_info, directory):
    if songs:
        # Save artist info
        artist_info_filepath = Artist.save_artist_info(artist_info, directory)

        # Save songs info
        songs_info_filepath = Track.save_songs_info(songs, artist_info.get('name'), directory)

        print(f"Artist: {artist_info.get('name')}")
        print(f"Artist Info File Path: {artist_info_filepath}")
        print(f"Songs Info File Path: {songs_info_filepath}")
    else:
        print(f"No songs found for artist '{artist_info.get('name')}'.")

def extract():
    start_time = time.time()
    # Define the directory path
    directory = config['datalake']['silver']
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Get top artists
    top_artists = Artist.get_top_artists(spotify)

    #Process each artist
    for artist_info in top_artists:
        artist_name = artist_info.get('name')
        artist_id = artist_info.get('id')
        # Get songs from the artist
        songs = Artist.get_all_artist_songs(artist_id, artist_name, spotify)
        #load files
        load(songs, artist_info, directory)
        print()  
    elapsed_time = time.time() - start_time
    print("Load is completed")   
    Artist.create_artist_genre_df(directory)
    Album.create_album_market_df(directory)
    print(f"Elapsed time: {elapsed_time} seconds")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('dashfy/spotifyextract/config.ini')

    api_conn = APIConn()
    spotify = api_conn.spotify

    extract()
