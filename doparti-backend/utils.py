from datetime import datetime
from dateutil import parser
import pytz

ARG_TZ = pytz.timezone("America/Argentina/Buenos_Aires")

def transformar_partido(match):
    utc_time = parser.parse(match["utcDate"])
    local_time = utc_time.astimezone(ARG_TZ)

    status = match["status"]

    if status == "FINISHED":
        estado = "finished"
    elif status in ["IN_PLAY", "PAUSED"]:
        estado = "live"
    else:
        estado = "upcoming"

    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]

    score_home = match["score"]["fullTime"]["home"]
    score_away = match["score"]["fullTime"]["away"]

    # Si está en vivo usamos el marcador actual
    if estado == "live":
        score_home = match["score"]["fullTime"]["home"]
        score_away = match["score"]["fullTime"]["away"]

    return {
        "id": match["id"],
        "liga": match["competition"]["name"],
        "hora": local_time.strftime("%H:%M"),
        "datetime": local_time,
        "estado": estado,
        "home": home,
        "away": away,
        "score_home": score_home,
        "score_away": score_away,
        "canal_url": f"https://link-del-canal.com/{match['id']}"  # placeholder
    }


def ordenar_partidos(partidos):
    terminados = [p for p in partidos if p["estado"] == "finished"]
    en_vivo = [p for p in partidos if p["estado"] == "live"]
    proximos = [p for p in partidos if p["estado"] == "upcoming"]

    terminados.sort(key=lambda x: x["datetime"])
    en_vivo.sort(key=lambda x: x["datetime"])
    proximos.sort(key=lambda x: x["datetime"])

    return terminados + en_vivo + proximos