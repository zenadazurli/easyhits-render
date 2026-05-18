from seleniumbase import SB
import requests
import time
import os

PROXY = "sazz16014w96:t3vz152mql23@resi.fusionproxy.net:13822"
EMAIL = "sandrominori50+ulugarecexisa@gmail.com"
PASSWORD = "DDnmVV45!!"
LOGIN_URL = "https://www.easyhits4u.com/logon/"

def get_turnstile_token():
    with SB(uc=True, headless=True, xvfb=True, block_images=True) as sb:
        sb.activate_cdp_mode(LOGIN_URL, proxy=PROXY)
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
            raise Exception("Token non trovato")
        return token

def login_with_token(token):
    session = requests.Session()
    data = {"username": EMAIL, "password": PASSWORD, "cf-turnstile-response": token}
    headers = {"User-Agent": "Mozilla/5.0"}
    proxies = {"http": f"http://{PROXY}", "https": f"http://{PROXY}"}
    r = session.post(LOGIN_URL, data=data, headers=headers, proxies=proxies, allow_redirects=False)
    return session.cookies.get_dict().get("sesids"), session.cookies.get_dict().get("user_id")

def main():
    print("🔄 Avvio...")
    token = get_turnstile_token()
    print("✅ Token ottenuto")
    sesids, user_id = login_with_token(token)
    if sesids and user_id:
        print(f"🎉 SUCCESSO! sesids={sesids} user_id={user_id}")
    else:
        print("❌ Fallito")

if __name__ == "__main__":
    main()