import pandas as pd
import os
import glob

class Track:

    def get_tracks_info(track_ids, spotify):
        track_info = spotify.tracks(track_ids)
        return track_info
    
    def get_songs_info():
        # Get all files that match the pattern "*_songs.parquet"
        songs_files = glob.glob('/home/matheusmatos/dashfy/datalake/silver/*_songs.parquet')
        # Create an empty list to store the DataFrames
        dfs = []
        # Iterate over info_files and append each DataFrame to the list
        for file in songs_files:
            df = pd.read_parquet(file)
            dfs.append(df)
        # Concatenate all DataFrames in the list
        df_songs = pd.concat(dfs)
        return df_songs
    
    def save_songs_info(songs, artist_name, directory):
        # Create DataFrame
        df_songs = pd.DataFrame(songs)
        artist_name = artist_name.replace(" ", "")
        artist_name = artist_name.replace("/", "-")  # Replace "/" with "-"
        # Set file path
        songs_info_filepath = os.path.join(directory, f"{artist_name}_songs.parquet")

        # Save DataFrame as Parquet File
        df_songs.to_parquet(songs_info_filepath, index=False)
        return songs_info_filepath
