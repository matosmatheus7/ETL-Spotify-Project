import pandas as pd 
from track import Track
import os
class Album:

    def get_tracks_id(album_id, spotify):
        tracks = spotify.album_tracks(album_id)
        track_ids = []

        for track in tracks['items']:
            track_ids.append(track.get('id'))
            
        return track_ids

    def create_album_market_df(directory):
        df = Track.get_songs_info()
        # Create a new DataFrame to store album names and available markets
        album_market_df = pd.DataFrame(columns=['album_name', 'available_markets'])

        # Iterate over each row in the original DataFrame
        for index, row in df.iterrows():
            album_name = row['album_name']
            markets_list = row['available_markets']

            # Create a temporary DataFrame for the current album and available markets
            temp_df = pd.DataFrame({'album_name': [album_name] * len(markets_list), 'available_markets': markets_list})

            # Concatenate the temporary DataFrame with the album_market_df DataFrame
            album_market_df = pd.concat([album_market_df, temp_df], ignore_index=True)
        
        album_market_filepath = os.path.join(directory, "album_market.parquet")
        # Save the DataFrame as a Parquet file
        album_market_df.to_parquet(album_market_filepath)
        
        # Print the success message
        print(f"The DataFrame 'album available markets' was saved successfully on: {album_market_filepath}")