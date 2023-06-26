import pandas as pd
import os
from album import Album
from track import Track
import glob

class Artist:

    def get_top_artists(spotify):
        limit = 50  # Maximum number of artists to retrieve per request
        offset = 0  # Starting offset for pagination
        top_artists = []  # List to store the top artists

        while len(top_artists) < 100:  # Continue until we have retrieved 100 artists
            results = spotify.search(q='year:2023', type='artist', limit=limit, offset=offset)
            items = results.get('artists').get('items')  # Extract the artists from the API response
            
            for artist in items:
                artist_info = {
                    'id': artist.get('id'),
                    'name': artist.get('name'),
                    'popularity': artist.get('popularity'),
                    'genres': artist.get('genres'),
                    'followers': artist['followers'].get('total')
                }
                top_artists.append(artist_info)  # Add the artist info to the top_artists list

            if len(items) < limit:
                # If the number of retrieved artists is less than the limit, it means there are no more artists to retrieve
                break

            offset += limit  # Increment the offset to retrieve the next page of artists

        return top_artists  # Return the top 100 artists

    def get_albums(artist_id, spotify):
        albums = spotify.artist_albums(artist_id, album_type='album')
        return albums

    def save_artist_info(artist_info, directory):
        # Create DataFrame
        df_artist = pd.DataFrame([artist_info])
        artist_name = artist_info.get('name').replace(" ", "")
        artist_name = artist_name.replace("/", "-")  # Replace "/" with "-"
        filename = f"{artist_name}_info.parquet"
        # Set file path
        artist_info_filepath = os.path.join(directory, filename)

        # Save DataFrame as Parquet File
        df_artist.to_parquet(artist_info_filepath, index=False)
        return artist_info_filepath

    def get_all_artist_songs(artist_id, artist_name, spotify):
        albums = Artist.get_albums(artist_id, spotify)
        songs = []
        if albums is None:
            # Handle the case where albums is None
            return []
        for album in albums['items']: 
            track_ids = Album.get_tracks_id(album.get('id'), spotify)
            track_info = Track.get_tracks_info(track_ids, spotify)

            for i in range(len(track_info['tracks'])):
                track = track_info['tracks'][i]
                song = {}
                song['song_id'] = track.get('id', 'Not Found')
                song['name'] = track.get('name', 'Not Found')
                song['artist'] = artist_name
                song['album_id'] = album.get('id', 'Not Found')
                song['album_name'] = album.get('name', 'Not Found')
                song['release_date'] = album.get('release_date', 'Not Found')
                song['available_markets'] = album.get('available_markets', 'Not Found')
                song['popularity'] = track.get('popularity', 'Not Found')
                songs.append(song)

        return songs

    def get_artists_info():
        # Get all files that match the pattern "*_info.parquet"
        artist_info = glob.glob('/home/matheusmatos/dashfy/datalake/silver/*_info.parquet')
        # Create an empty list to store the DataFrames
        dfs = []
        # Iterate over info_files and append each DataFrame to the list
        for file in artist_info:
            df = pd.read_parquet(file)
            dfs.append(df)
        # Concatenate all DataFrames in the list
        df_artists = pd.concat(dfs)
        return df_artists

    def create_artist_genre_df(directory):
        df = Artist.get_artists_info()
        # Create a new DataFrame to store artist names and genres
        artist_genre_df = pd.DataFrame(columns=['name', 'genre'])

        # Iterate over each row in the original DataFrame
        for index, row in df.iterrows():
            artist_name = row['name']
            genres_list = row['genres']

            # Create a temporary DataFrame for the current artist and genres
            temp_df = pd.DataFrame({'name': [artist_name] * len(genres_list), 'genre': genres_list})

            # Concatenate the temporary DataFrame with the artist_genre_df DataFrame
            artist_genre_df = pd.concat([artist_genre_df, temp_df], ignore_index=True)
        
        artist_genre_filepath = os.path.join(directory, "artist_genre.parquet")
        # Save the DataFrame as a Parquet file
        artist_genre_df.to_parquet(artist_genre_filepath)
        
        # Print the success message
        print(f"The DataFrame 'Artists Genres' was saved successfully on: {artist_genre_filepath}")