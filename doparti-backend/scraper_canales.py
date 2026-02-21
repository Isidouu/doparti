# scraper_canales.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def buscar_canal_partido(home, away):

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        print("🔎 Abriendo Promiedos...")

        driver.get("https://www.promiedos.com.ar")
        time.sleep(3)

        links = driver.find_elements(By.TAG_NAME, "a")

        partido_link = None

        for link in links:
            texto = link.text.lower()

            if home.lower().split()[0] in texto and away.lower().split()[0] in texto:
                partido_link = link.get_attribute("href")
                break

        if not partido_link:
            print("❌ No se encontró el link del partido")
            driver.quit()
            return None

        print("✅ Link encontrado:", partido_link)

        driver.get(partido_link)
        time.sleep(5)

        print("\n================ DOM DEBUG =================")
        print(driver.page_source[:8000])  # imprime parte del HTML renderizado
        print("================ END DEBUG ================\n")

        driver.quit()
        return None

    except Exception as e:
        print("🔥 Error Selenium:", e)
        driver.quit()
        return None