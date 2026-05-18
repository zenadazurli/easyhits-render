# cookie_refresh.py
import asyncio
import requests
from cloakbrowser.async_api import launch  # Usiamo l'API asincrona di CloakBrowser

# Configurazione del proxy FusionProxy (usa le tue credenziali)
PROXY_STRING = "socks5://sazz16014w96:t3vz152mql23@resi.fusionproxy.net:13822"

EMAIL = "sandrominori50+ulugarecexisa@gmail.com"
PASSWORD = "DDnmVV45!!"
LOGIN_URL = "https://www.easyhits4u.com/logon/"

async def get_turnstile_token():
    """Avvia CloakBrowser, ottiene il token e lo restituisce."""
    # Lancia il browser. La configurazione è cruciale:
    # - proxy: il nostro proxy residenziale
    # - headless: True (girerà senza interfaccia)
    # - geoip: True (allinea fuso orario e lingua al proxy)
    # - humanize: True (comportamento più umano)
    browser = await launch(
        proxy=PROXY_STRING,
        headless=True,
        geoip=True,
        humanize=True
    )
    page = await browser.new_page()
    
    try:
        await page.goto(LOGIN_URL)
        print("✅ Pagina caricata.")
        
        # Aspetta che i campi di input siano visibili (segno che Turnstile è risolto)
        await page.wait_for_selector('input[name="username"]', timeout=60000)
        print("✅ Turnstile risolto.")
        
        # Compila il form
        await page.fill('input[name="username"]', EMAIL)
        await page.fill('input[name="password"]', PASSWORD)
        
        # Invia il form premendo il tasto "Enter"
        await page.keyboard.press("Enter")
        print("🔑 Login inviato.")
        
        # Aspetta che la pagina si aggiorni (dopo il login)
        await page.wait_for_timeout(5000)
        
        # Estrae il token dal campo hidden
        token = await page.get_attribute('input[name="cf-turnstile-response"]', 'value')
        return token
    finally:
        await browser.close()

def login_with_token(token):
    """Invia la richiesta di login usando il token ottenuto."""
    session = requests.Session()
    data = {
        "username": EMAIL,
        "password": PASSWORD,
        "cf-turnstile-response": token
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://www.easyhits4u.com",
        "Referer": LOGIN_URL,
    }
    proxies = {"http": f"socks5://{PROXY_STRING.split('://')[1]}", 
               "https": f"socks5://{PROXY_STRING.split('://')[1]}"}
    r = session.post(LOGIN_URL, data=data, headers=headers, proxies=proxies, allow_redirects=False)
    return session.cookies.get_dict().get("sesids"), session.cookies.get_dict().get("user_id")

async def main():
    print("🔄 Avvio CloakBrowser per ottenere il token...")
    token = await get_turnstile_token()
    if not token:
        print("❌ Impossibile ottenere il token Turnstile.")
        return
    print(f"✅ Token ottenuto: {token[:50]}...")
    
    print("🔑 Invio richiesta di login...")
    sesids, user_id = login_with_token(token)
    if sesids and user_id:
        print(f"🎉 SUCCESSO! sesids={sesids}, user_id={user_id}")
    else:
        print("❌ Login fallito.")

if __name__ == "__main__":
    asyncio.run(main())
