# canales.py

CANALES = {
    "ESPN Premium": "https://tvlibree.com/en-vivo/espn-premium/#pc",
    "TNT Sports": "https://tvlibree.com/en-vivo/tnt-sports/#pc",
    "TyC Sports": "https://tvlibree.com/en-vivo/tyc-sports/#pc",
    "ESPN 2": "https://tvlibree.com/en-vivo/espn-2-ar/",
    "Fox Sports 2": "https://tvlibree.com/en-vivo/fox-sports/#2",
    "Fox Sports 3": "https://tvlibree.com/en-vivo/fox-sports-3/",
    "ESPN 5": "https://tvlibree.com/en-vivo/espn-5/#pc",
    "ESPN 6": "https://tvlibree.com/en-vivo/espn-6/#pc",
    "ESPN 7": "https://tvlibree.com/en-vivo/espn-7/#pc",
    "DSports 2": "https://tvlibree.com/en-vivo/dsports-2/",
    "ESPN": "https://tvlibree.com/en-vivo/espn/#pc",
    "ESPN 3": "https://tvlibree.com/en-vivo/espn-3/#pc",
    "ESPN 4": "https://tvlibree.com/en-vivo/espn-4/#pc",
    "Dsports": "https://tvlibree.com/en-vivo/dsports/#2",
    "Fox Sports": "https://tvlibree.com/en-vivo/fox-sports/#2",
    "Disney+": "https://tvlibree.com/eventos/?r=aHR0cHM6Ly9zdHJlYW10cDEwLmNvbS9nbG9iYWwxLnBocD9zdHJlYW09ZGlzbmV5Mg=="
}


def obtener_link_oficial(nombre_detectado):
    if not nombre_detectado:
        return None

    nombre_detectado = nombre_detectado.lower()

    for nombre, link in CANALES.items():
        if nombre.lower() in nombre_detectado:
            return link

    return None