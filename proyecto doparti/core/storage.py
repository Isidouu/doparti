import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
MATCHES_PATH = os.path.join(BASE_DIR, "matches.json")


# =========================
# CONFIG
# =========================

DEFAULT_CONFIG = {
    "favorite_team": None,
    "followed_teams": [],
    "followed_leagues": [],
    "notifications": {
        "60_min": True,
        "30_min": True,
        "10_min": True,
        "kickoff": True
    }
}


def initialize_storage():
    """Crea archivos base si no existen."""
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

    if not os.path.exists(MATCHES_PATH):
        with open(MATCHES_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config_data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)


# =========================
# MATCHES
# =========================

def load_matches():
    with open(MATCHES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_matches(matches):
    with open(MATCHES_PATH, "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=4)


def update_match(match_id, updates: dict):
    matches = load_matches()
    updated = False

    for match in matches:
        if match["id"] == match_id:
            match.update(updates)
            updated = True
            break

    if updated:
        save_matches(matches)

    return updated


def add_or_update_match(match_data: dict):
    matches = load_matches()
    found = False

    for i, match in enumerate(matches):
        if match["id"] == match_data["id"]:
            matches[i] = match_data
            found = True
            break

    if not found:
        matches.append(match_data)

    save_matches(matches)


# =========================
# UTILIDADES
# =========================

def match_exists(match_id):
    matches = load_matches()
    return any(m["id"] == match_id for m in matches)


def remove_old_matches():
    """Elimina partidos ya finalizados (más de 1 día viejo)."""
    matches = load_matches()
    now = datetime.utcnow()

    filtered = []
    for match in matches:
        kickoff = datetime.fromisoformat(match["kickoff"])
        if (now - kickoff).total_seconds() < 86400:
            filtered.append(match)

    save_matches(filtered)
