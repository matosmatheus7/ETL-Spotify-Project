from flask import Flask, render_template
import glob
import pandas as pd

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

def get_artist_genre():
    # Get all files that match the pattern "*_songs.parquet"
    artist_genre = glob.glob('/home/matheusmatos/dashfy/datalake/silver/artist_genre.parquet')
    # Create an empty list to store the DataFrames
    dfs = []
    # Iterate over info_files and append each DataFrame to the list
    for file in artist_genre:
        df = pd.read_parquet(file)
        dfs.append(df)
    # Concatenate all DataFrames in the list
    df_artist_genre = pd.concat(dfs)
    return df_artist_genre

def get_most_followed_artists(df):
    # Top 5 Artists with more followers on spotify 
    highly_followed_artists = df[["name", "followers"]].sort_values('followers', ascending=False).head(5)
    return highly_followed_artists.to_dict('records')

def get_most_popular_artists(df):
    # Top 5 Artists with more pupularity score on spotify 
    popular_artist = df[["name", "popularity"]].sort_values('popularity', ascending=False).head(5)
    return popular_artist.to_dict('records')

def get_most_popular_songs(df):
    # Top 5 Artists with more pupularity score on spotify 
    popular_songs = df[["artist", "name", "popularity"]].sort_values('popularity', ascending=False).head(5)
    return popular_songs.to_dict('records')

def get_most_popular_albums(df):
    # Top 5 Albums with more pupularity score on spotify 
    df_album_popularity = df.groupby('album_name').agg({ 'artist':'first', 'album_name': 'first','popularity': 'median'}).round(1).sort_values('popularity', ascending=False).head(5)
    return df_album_popularity.to_dict('records')

def get_most_songful_artists(df):
    # Top 5 artists with more musics on spotify 
    artist_songs_count = df["artist"].value_counts().sort_values(ascending=False).head(5)
    artist_songs_count = artist_songs_count.reset_index()
    artist_songs_count.columns = ["artist", "songs_count"]
    return artist_songs_count.to_dict('records')

def filter_by_genre(df, genre_to_be_filtered):
    # Convert the 'genre' column to string type
    df['genre'] = df['genre'].astype(str)
    # Add the count of genres that contains genre_to_be_filtered to the genre_to_be_filtered count
    genre_to_be_filtered_count = df.loc[df['genre'].str.contains(genre_to_be_filtered, case=False), 'artist_count'].sum()
    # Update the count for the genre_to_be_filtered genre
    df.loc[df['genre'] == genre_to_be_filtered, 'artist_count'] = genre_to_be_filtered_count
    # Exclude the rows that contain genre_to_be_filtered except for the row with genre genre_to_be_filtered
    df = df[~(df['genre'].str.contains(genre_to_be_filtered, case=False) & (df['genre'] != genre_to_be_filtered))]
    return df

def group_others_genres(df, threshold):
    one_artist_genres = df[df['artist_count'] < threshold]['genre']
    df.loc[df['genre'].isin(one_artist_genres), 'genre'] = 'Others'
    df = df.groupby('genre').sum().reset_index()
    return df
    
    # filtar top 10 e mostrar o restante como outros
def get_popular_genres(df):
    popular_genres = df['genre'].value_counts().reset_index()
    popular_genres.columns = ["genre", "artist_count"]
    popular_genres = filter_by_genre(popular_genres, "rap")
    popular_genres = filter_by_genre(popular_genres, "pop")
    popular_genres = filter_by_genre(popular_genres, "rock")
    popular_genres = filter_by_genre(popular_genres, "r&b")
    popular_genres = filter_by_genre(popular_genres, "hip hop")
    popular_genres = filter_by_genre(popular_genres, "country")
    popular_genres = filter_by_genre(popular_genres, "sertanejo")
    popular_genres = filter_by_genre(popular_genres, "house")
    popular_genres = filter_by_genre(popular_genres, "eletronic")
    popular_genres = filter_by_genre(popular_genres, "house")
    popular_genres = group_others_genres(popular_genres, 5)
    return popular_genres

app = Flask(__name__)

@app.route('/')
def index():
    df_artists = get_artists_info()
    highly_followed_artists = get_most_followed_artists(df_artists)
    popular_artist = get_most_popular_artists(df_artists)
    
    df_songs = get_songs_info()
    popular_songs = get_most_popular_songs(df_songs)
    artist_songs_count = get_most_songful_artists(df_songs)
    album_popularity = get_most_popular_albums(df_songs)
    df_artist_genres = get_artist_genre()
    popular_genres = get_popular_genres(df_artist_genres)
    # Extract the relevant data for the chart
    labels = popular_genres['genre'].tolist()
    values = popular_genres['artist_count'].tolist()
    return render_template('index.html', album_popularity=album_popularity, highly_followed_artists=highly_followed_artists, popular_artist=popular_artist, popular_songs=popular_songs, artist_songs_count=artist_songs_count, labels=labels, values=values)

if __name__ == '__main__':
    app.run(debug=True)
    