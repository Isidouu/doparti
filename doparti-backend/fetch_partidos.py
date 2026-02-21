# fetch_partidos.py

import requests

BASE_URL = "https://api.football-data.org/v4"
API_KEY = "17cb7cbcc31049bc9e7c2f9c06610127"  # asegurate que esté correcta


def fetch_partidos():
    headers = {
        "X-Auth-Token": API_KEY
    }

    try:
        response = requests.get(
            f"{BASE_URL}/matches",
            headers=headers,
            timeout=10
        )

        print("STATUS CODE:", response.status_code)

        if response.status_code != 200:
            print("ERROR RESPONSE:", response.text)
            return {"error": "No se pudieron obtener partidos"}

        data = response.json()

        partidos = []

        for match in data.get("matches", []):
            partidos.append({
                "id": match["id"],
                "liga": match["competition"]["name"],
                "matchday": match.get("matchday"),
                "hora": match["utcDate"],
                "estado": match["status"],
                "home": match["homeTeam"]["name"],
                "away": match["awayTeam"]["name"],
                "score": match.get("score", {})
            })

        return partidos

    except Exception as e:
        print("ERROR REAL:", e)
        return {"error": "No se pudieron obtener partidos"}