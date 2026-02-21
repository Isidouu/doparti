import requests
from datetime import datetime, timedelta

SOFASCORE_BASE = "https://api.sofascore.com/api/v1"


def get_matches_by_date(date: datetime):
    date_str = date.strftime("%Y-%m-%d")
    url = f"{SOFASCORE_BASE}/sport/football/scheduled-events/{date_str}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "Referer": "https://www.sofascore.com/",
        "Origin": "https://www.sofascore.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error obteniendo partidos:", response.status_code)
        return []

    data = response.json()
    matches = []

    for event in data.get("events", []):
        match = {
            "id": str(event["id"]),
            "league": event["tournament"]["name"],
            "home": event["homeTeam"]["name"],
            "away": event["awayTeam"]["name"],
            "kickoff": datetime.utcfromtimestamp(
                event["startTimestamp"]
            ).isoformat(),
            "channel": None,
            "notified_60": False,
            "notified_30": False,
            "notified_10": False,
            "notified_kickoff": False
        }

        matches.append(match)

    return matches


def get_next_days_matches(days=3):
    all_matches = []

    for i in range(days):
        date = datetime.utcnow() + timedelta(days=i)
        day_matches = get_matches_by_date(date)
        all_matches.extend(day_matches)

    return all_matches
