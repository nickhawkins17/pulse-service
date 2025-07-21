import argparse

import pandas
import requests
from sqlalchemy import create_engine

from .access_token import get_spotify_token

SPOTIFY_API_URL = "https://api.spotify.com/v1/"
SPOTIFY_PLAYLISTS = "playlists"
POSTGRES_TRACKS = "tracks"


def fetch_playlist(playlist_id):
    access_token, token_type = get_spotify_token()
    url = f"{SPOTIFY_API_URL}{SPOTIFY_PLAYLISTS}/{playlist_id}/tracks"
    headers = {"Authorization": f"{token_type} {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch playlist: {response.status_code} - {response.text}")
        return None


def convert_to_df(playlist_data):
    # Extract track details for DataFrame
    records = []
    for item in playlist_data.get("items", []):
        track = item.get("track", {})
        records.append(
            {
                "track_name": track.get("name"),
                "artist_names": [artist["name"] for artist in track.get("artists", [])],
                "album_name": track.get("album", {}).get("name"),
                "track_id": track.get("id"),
                "uri": track.get("uri"),
            }
        )

    return pandas.DataFrame(records)


def df_to_postgres(df, db_url, table_name):
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"Inserted {len(df)} records into {table_name} table.")


def main():
    parser = argparse.ArgumentParser(description="Fetch Spotify playlist and load tracks to Postgres")
    parser.add_argument("playlist_id", help="Spotify playlist ID (e.g., 2NH9p4zPryokG9QWG7cHKb)")
    parser.add_argument(
        "--db-url",
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/pulse",
        help="Database URL for Postgres connection",
    )
    args = parser.parse_args()

    playlist_data = fetch_playlist(args.playlist_id)
    playlist_df = convert_to_df(playlist_data)
    df_to_postgres(playlist_df, args.db_url, POSTGRES_TRACKS)


if __name__ == "__main__":
    main()
