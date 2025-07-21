import argparse
import os

import redis
import requests
from dotenv import load_dotenv

# Connect to your local Redis server (adjust host/port if needed)
r = redis.Redis(host="localhost", port=6379, db=0)

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

SPOTIFY_ACCOUNTS_URL = "https://accounts.spotify.com/api/token"


def fetch_and_store_spotify_token():
    # Step 1: Request the token
    payload = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(SPOTIFY_ACCOUNTS_URL, data=payload, headers=headers)
    data = response.json()
    access_token = data["access_token"]
    token_type = data["token_type"]
    expires_in = data["expires_in"]  # typically 3600 seconds

    # Step 2: Store in Redis with TTL
    r.set("spotify:access_token", access_token, ex=expires_in)
    r.set("spotify:token_type", token_type, ex=expires_in)

    print("Token stored in Redis with TTL of", expires_in, "seconds.")


def get_spotify_token():
    access_token = r.get("spotify:access_token")
    token_type = r.get("spotify:token_type")
    if access_token and token_type:
        return access_token.decode(), token_type.decode()
    else:
        print("Token not found or expired.")
        return None, None


def main():
    parser = argparse.ArgumentParser(description="Spotify Token Utility")
    parser.add_argument("--generate", action="store_true", help="Generate and store a new Spotify access token")
    args = parser.parse_args()

    if args.generate:
        fetch_and_store_spotify_token()

    token, token_type = get_spotify_token()
    print("Token:", token)
    print("Type:", token_type)


if __name__ == "__main__":
    main()
