#!/usr/bin/env python3
# cookie_refresh.py - Genera cookie per EasyHits4U su Render usando proxy residenziale

import time
import requests
import random

from seleniumbase import SB

# ========= CONFIGURAZIONE =========
# Proxy FusionProxy (lista di porte per rotazione)
PROXY_LIST = [
    "sazz16014w96:t3vz152mql23@resi.fusionproxy.net:13822",
    "sazz16014w96:t3vz152mql23@resi.fusionproxy.net:14693",
    "sazz16014w96:t3vz152mql23@resi.fusionproxy.net:13711",
    "sazz16014w96:t3vz152mql23@resi.fusionproxy.net:14329",
    "sazz16014w96:t3vz152mql23@resi.fusionproxy.net:14012",
    "sazz16014w96:t3vz152mql23@resi.fusionproxy.net:14465",
    "sazz16014w96:t3vz152mql23@resi.fusionproxy.net:13768",
    "sazz16014w96:t3vz152mql23@resi.fusionproxy.net:13506",
    "sazz16014w96:t3vz152mql23@resi.fusionproxy.net:14995",
    "sazz16014w96:t3vz152mql23@resi.fusionproxy.net:13353",
]

EMAIL = "sandrominori50+ulugarecexisa@gmail.com"
PASSWORD = "DDnmVV45!!"
LOGIN_URL = "https://www.easyhits4u.com/logon/"

# Opzionale: Supabase (commenta se non lo usi)
import os
from supabase import create_client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
ACCOUNT_NAME = "uujkrczveemscvo"

# ========= FUNZIONI =========
def get_turnstile_token(proxy):
    """Apre il browser con il proxy, aspetta il token Turnstile e lo restituisce"""
    with SB(uc=True, headless=True, xvfb=True, block_images=True) as sb:
        sb.activate_cdp_mode(LOGIN_URL, proxy=proxy)
        sb.wait_for_element_visible('input[name="username"]', timeout=60)
        sb.type('input[name="username"]', EMAIL)
        sb.type('input[name="password"]', PASSWORD)

        token = None
        for _ in range(30):
            token = sb.get_attribute('input[name="cf-turnstile-response"]', 'value')
            if token and len(token) > 50:
                break
            time.sleep(1)
        if not token:
            raise Exception("Token Turnstile non trovato")
        print(f"✅ Token ottenuto: {token[:50]}...")
        return token

def login_with_token(token, proxy):
    """Invia il form usando il token (HTTP, senza browser)"""
    session = requests.Session()
    data = {
        "username": EMAIL,
        "password": PASSWORD,
        "cf-turnstile-response": token,
        "manual": "1"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://www.easyhits4u.com",
        "Referer": LOGIN_URL,
    }
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    r = session.post(LOGIN_URL, data=data, headers=headers, proxies=proxies, allow_redirects=False)
    cookies = session.cookies.get_dict()
    return cookies.get("sesids"), cookies.get("user_id")

def save_to_supabase(sesids, user_id):
    """Salva i cookie su Supabase (opzionale)"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    cookie_string = f"sesids={sesids}; user_id={user_id}"
    supabase.table("account_cookies").upsert({
        "account_name": ACCOUNT_NAME,
        "cookies_string": cookie_string,
        "status": "active"
    }).execute()
    print("💾 Cookie salvati su Supabase")

# ========= MAIN =========
def main():
    # Scegli una porta proxy a caso
    proxy = random.choice(PROXY_LIST)
    print(f"🔑 Proxy scelto: {proxy.split('@')[1]}")

    try:
        token = get_turnstile_token(proxy)
        sesids, user_id = login_with_token(token, proxy)

        if sesids and user_id:
            print(f"\n🎉 SUCCESSO!\nsesids={sesids}\nuser_id={user_id}")
            save_to_supabase(sesids, user_id)
        else:
            print("\n❌ Login fallito: cookie non ricevuti")
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")

if __name__ == "__main__":
    main()
