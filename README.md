# Pulse

The **pulse-service** provides data management and RESTful services for a platform to review Spotify content.

## Table of Contents

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

## References
