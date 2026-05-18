import time
import requests
from cloakbrowser import launch

PROXY = "socks5://sazz16014w96:t3vz152mql23@resi.fusionproxy.net:13822"

EMAIL = "sandrominori50+ulugarecexisa@gmail.com"
PASSWORD = "DDnmVV45!!"
LOGIN_URL = "https://www.easyhits4u.com/logon/"

def get_turnstile_token():
    # geoip=False per evitare la dipendenza mancante (ma perdiamo un po' di stealth)
    browser = launch(
        proxy=PROXY,
        headless=True,
        geoip=False,
        humanize=True
    )
    page = browser.new_page()
    try:
        page.goto(LOGIN_URL)
        print("✅ Pagina caricata.")
        page.wait_for_selector('input[name="username"]', timeout=60000)
        print("✅ Turnstile risolto.")
        page.fill('input[name="username"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        page.keyboard.press("Enter")
        print("🔑 Login inviato.")
        time.sleep(5)
        token = page.get_attribute('input[name="cf-turnstile-response"]', 'value')
        return token
    finally:
        browser.close()

def login_with_token(token):
    session = requests.Session()
    data = {"username": EMAIL, "password": PASSWORD, "cf-turnstile-response": token}
    headers = {"User-Agent": "Mozilla/5.0"}
    proxies = {"http": PROXY, "https": PROXY}
    r = session.post(LOGIN_URL, data=data, headers=headers, proxies=proxies, allow_redirects=False)
    return session.cookies.get_dict().get("sesids"), session.cookies.get_dict().get("user_id")

def main():
    print("🔄 Avvio CloakBrowser...")
    token = get_turnstile_token()
    if not token:
        print("❌ Token non ottenuto")
        return
    print(f"✅ Token: {token[:50]}...")
    sesids, user_id = login_with_token(token)
    if sesids and user_id:
        print(f"🎉 SUCCESSO! sesids={sesids} user_id={user_id}")
    else:
        print("❌ Login fallito")

if __name__ == "__main__":
    main()
