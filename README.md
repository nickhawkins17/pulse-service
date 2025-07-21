# Pulse

The **pulse-service** provides data management and RESTful services for a platform to review Spotify content.

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [References](#references)

## Prerequisites

- [Python](https://www.python.org/downloads/release/python-31211/) (via [pyenv](https://formulae.brew.sh/formula/pyenv))
- [Orbstack](https://orbstack.com/)

## Setup

Create the Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Setup environment variables:

```bash
# Create `.env` and apply any necessary changes:
cp .env_template .env
```

## Usage

### Services

- Start services: `make up`
- Stop services: `make down`

### Utilities

#### Spotify

- Generate access token: `make token`
- Get access token: `make get-token`
- Ingest songs from playlist to local db: `make ingest playlist_id=<Spotify Playlist ID>`

#### Alembic

- Upgrade migrations: `make upgrade-db`

## References
