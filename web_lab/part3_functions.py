# Laborator: funcții, metode și importuri pe web
# Student: Grigorița Alexandra
from pydoc import html
import time
from typing import Dict, List, Optional

import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


# Exercițiul 21. 
print("Ex 21")
def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Efectuează o cerere GET către adresa url furnizată."""
    return requests.get(url, timeout=timeout)

r21 = fetch(BASE_URL)
print("Fetch status:", r21.status_code)

# Exercițiul 22. 
print("Ex 22")
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


for path in ["/", "/robots.txt", "/sitemap.xml"]:
    print(f"Status pt {path}:", get_status(BASE_URL + path))
    time.sleep(1)

# Exercițiul 23. Parametri impliciți
print("Ex 23")
def fetch_with_timeout(url: str, timeout: int = 10) -> requests.Response:
    """Efectuează o cerere GET cu timeout implicit configurabil."""
    return requests.get(url, timeout=timeout)


print("Status cu timeout implicit:", fetch_with_timeout(BASE_URL).status_code)
print("Status cu timeout=3:", fetch_with_timeout(BASE_URL, timeout=3).status_code)

#exercitiu 24
print("Ex 24")
def get_title(html):
    """Returnează titlul paginii dintr-un șir HTML (șir gol dacă lipsește)."""
    start = html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = html.find("</title>", start)
    return html[start:end].strip()


# Test fără rețea, pe un HTML scris de noi
test_html = "<html><head><title>  Pagina mea  </title></head></html>"
print(get_title(test_html))  # Pagina mea

# Test pe site-ul real: descărcarea se face în afara funcției
response = requests.get(BASE_URL, timeout=TIMEOUT)
print(get_title(response.text))

#exercitiu 25
print("Ex25")
def get_title(html):
    """Returnează titlul paginii dintr-un șir HTML."""
    start = html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = html.find("</title>", start)
    return html[start:end].strip()

help(get_title)

#exercitiu 26
print("Ex 26")

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


print("Apel corect:", get_status(BASE_URL))  # 200

# Apel cu tipul greșit (int în loc de str):
try:
    print(get_status(123))
except Exception as e:
    print("Eroare la rulare:", type(e).__name__)  # MissingSchema
    
    
# exercițiul 27
print("Ex 27")


def page_exists(url: str) -> bool:
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return res.status_code == 200
    except requests.RequestException:
        return False

print("Cybercor există?", page_exists(BASE_URL))
print("Domeniul invalid exista?", page_exists("https://this-domain-does-not-exist.invalid"))



# Exercițiul 28. Returnarea unui dicționar
print("Ex 28")
def check_paths(base: str, paths: List[str]) -> Dict[str, int]:
    results = {}
    for path in paths:
        full_url = base + path
        try:
            res = requests.get(full_url, timeout=TIMEOUT)
            results[path] = res.status_code
        except requests.RequestException:
            results[path] = 0
        time.sleep(1)
    return results
paths_to_check = ["/", "/robots.txt", "/sitemap.xml"]
print("Rezultatele verificării path-urilor:", check_paths(BASE_URL, paths_to_check))


print("Check paths:", check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

# Exercițiul 29. Argumente cu nume
print("Ex 29")
def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returnează valoarea unui antet specific de la o adresă URL."""
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return res.headers.get(name, default)
    except requests.RequestException:
        return default


print("Antet Server:", get_header(BASE_URL, name="Server"))

# Exercițiul 30. Antete de securitate
print("Ex 30")
def security_headers(url: str) -> Dict[str, bool]:
    """Verifică prezența celor 5 antete fundamentale de securitate."""
    sec_list = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return {h: h in res.headers for h in sec_list}
    except requests.RequestException:
        return {h: False for h in sec_list}

sec_res = security_headers(BASE_URL)
print("Antete securitate:", sec_res)

# Exercițiul 31. Funcții care apelează funcții
print("Ex 31")
def score_headers(results: Dict[str, bool]) -> str:
    """Calculează scorul de securitate sub formă de fracție text (ex: '3/5')."""
    passed = sum(1 for val in results.values() if val)
    return f"{passed}/{len(results)}"


print("Scor securitate:", score_headers(sec_res))

# Exercițiul 32. Două funcții, o sarcină
print("Ex 32")
def fetch_robots(base: str) -> Optional[str]:
    """Descarcă fișierul robots.txt de pe un site."""
    try:
        res = requests.get(base.rstrip('/') + "/robots.txt", timeout=TIMEOUT)
        if res.status_code == 200:
            return res.text
        return None
    except requests.RequestException:
        return None

def disallowed_paths(robots_text: Optional[str]) -> List[str]:
    """Extrage căile blocate (Disallow) din fișierul robots.txt."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                val = parts[1].strip()
                if val:
                    paths.append(val)
    return paths


r_text = fetch_robots(BASE_URL)
print("Disallowed paths:", disallowed_paths(r_text))

# Exercițiul 33. Oricâte argumente
print("Ex 33")
def response_times(*urls: str) -> Dict[str, float]:
    """Măsoară timpul de răspuns pentru un număr nedeterminat de adrese URL."""
    times = {}
    for url in urls:
        try:
            start = time.perf_counter()
            requests.get(url, timeout=TIMEOUT)
            duration = time.perf_counter() - start
            times[url] = round(duration, 4)
        except requests.RequestException:
            times[url] = -1.0
        time.sleep(1)
    return times


print("Timpi răspuns:", response_times(BASE_URL, ECHO_URL))

# Exercițiul 34.
print("Ex 34")
def log(message: str, **details) -> None:
    """Afișează un mesaj de jurnalizare formatat cu detaliile primite."""
    formatted_details = " | ".join(f"{k}={v}" for k, v in details.items())
    if formatted_details:
        print(f"{message} | {formatted_details}")
    else:
        print(message)


log("verificat", url=BASE_URL, status=200)