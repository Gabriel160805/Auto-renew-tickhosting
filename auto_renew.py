from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Leer cookie desde el secreto de GitHub
SESSION_COOKIE = os.getenv('PTERODACTYL_SESSION', '')

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    # User-Agent realista para intentar evadir detección
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    return webdriver.Chrome(options=options)

def main():
    driver = None
    try:
        print("Iniciando navegador...")
        driver = setup_driver()
        driver.set_page_load_timeout(30)

        print("Navegando a tickhosting.com...")
        driver.get("https://tickhosting.com/")
        time.sleep(5)

        print("Añadiendo cookie...")
        driver.delete_all_cookies()
        try:
            driver.add_cookie({
                'name': 'pterodactyl_panel_session',
                'value': SESSION_COOKIE,
                'domain': 'tickhosting.com'
            })
            print("Cookie añadida correctamente.")
        except Exception as e:
            print(f"Error al añadir cookie: {e}")

        print("Recargando página...")
        driver.refresh()
        time.sleep(8)

        print(f"URL actual: {driver.current_url}")
        print(f"Título de la página: {driver.title}")

        # Guardar captura
        driver.save_screenshot('debug_login_test.png')
        print("Captura guardada como debug_login_test.png")

        # Guardar HTML para inspección
        with open('debug_login_page.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("HTML guardado como debug_login_page.html")

    except Exception as e:
        print(f"Error general: {e}")
        if driver:
            driver.save_screenshot('debug_error.png')
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
