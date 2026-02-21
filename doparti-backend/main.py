# main.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fetch_partidos import fetch_partidos
from scraper_canales import buscar_canal_partido
from canales import obtener_link_oficial
from cache_manager import get_from_cache, save_to_cache
from datetime import datetime
import pytz

app = FastAPI()

ARG_TZ = pytz.timezone("America/Argentina/Buenos_Aires")

PARTIDOS_CACHE = []  # 🔥 memoria


def formatear_fecha_hora(utc_string):
    utc_dt = datetime.strptime(utc_string, "%Y-%m-%dT%H:%M:%SZ")
    utc_dt = pytz.utc.localize(utc_dt)
    arg_dt = utc_dt.astimezone(ARG_TZ)

    return (
        arg_dt.strftime("%d/%m/%Y"),
        arg_dt.strftime("%I:%M %p"),
        int(arg_dt.timestamp())
    )


@app.get("/", response_class=HTMLResponse)
def home():
    global PARTIDOS_CACHE

    if not PARTIDOS_CACHE:  # 🔥 solo llama si está vacío
        partidos = fetch_partidos()

        if isinstance(partidos, dict):
            return "<h1>Error obteniendo partidos</h1>"

        PARTIDOS_CACHE = partidos

    html = "<h1>Partidos del día</h1>"

    for p in PARTIDOS_CACHE:
        fecha, hora, timestamp = formatear_fecha_hora(p["hora"])

        html += f"""
        <div>
            <h3>{p['home']} vs {p['away']}</h3>
            <p>{fecha} - {hora}</p>
            <a href="/ver/{p['id']}">Ver partido</a>
            <hr>
        </div>
        """

    return html


@app.get("/ver/{partido_id}", response_class=HTMLResponse)
def ver_partido(partido_id: int):
    global PARTIDOS_CACHE

    partido = next((p for p in PARTIDOS_CACHE if p["id"] == partido_id), None)

    if not partido:
        return "<h1>Partido no encontrado</h1>"

    canal_detectado = buscar_canal_partido(partido["home"], partido["away"])
    canal_url = obtener_link_oficial(canal_detectado) or "https://tvlibree.com"

    return HTMLResponse(f"""
        <h1>{partido['home']} vs {partido['away']}</h1>
        <p>Canal: {canal_detectado or "No especificado"}</p>
        <a href="{canal_url}">Ir al partido</a>
    """)