import hashlib
import json
import re
import socket
import ssl
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


# ex 35
print("Ex 35")
parts = urlparse("https://cybercor.org/path?x=1#top")
print("scheme:  ", parts.scheme)
print("netloc:  ", parts.netloc)
print("path:    ", parts.path)
print("query:   ", parts.query)
print("fragment:", parts.fragment)

#ex 36
print("Ex 36")
for link in ["/about", "contact.html", "../index.html"]:
    print(link, "->", urljoin(BASE_URL, link))


# ex 37

def extract_links(html: str) -> list:
    raw_links = re.findall(r'href="([^"]+)"', html)
    unique_links = list(dict.fromkeys(raw_links))
    return unique_links

res_37 = requests.get(BASE_URL, timeout=TIMEOUT)
found_links = extract_links(res_37.text)
print(f"S-au găsit {len(found_links)} legături unice. Primele 5:")
for link in found_links[:5]:
    print(" -", link)

# ex 38

def split_links(links: list, domain: str):
    """Împarte legăturile în (interne, externe) față de domeniul dat."""
    internal, external = [], []
    for link in links:
        full = urljoin("https://" + domain, link)
        if urlparse(full).netloc == domain:
            internal.append(full)
        else:
            external.append(full)
    return internal, external


response = requests.get(BASE_URL, timeout=TIMEOUT)
links = extract_links(response.text)
internal, external = split_links(links, "cybercor.org")
print("Ex 37:", len(links), "legături unice")
print("Ex 38:", len(internal), "interne,", len(external), "externe")


# ex 39
print("Ex 39")
class ImageFinder(HTMLParser):
    """Colectează atributul src al fiecărui tag <img>."""

    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        # HTMLParser transformă numele tag-urilor și atributelor în litere mici,
        # deci <IMG SRC=...> ajunge aici ca tag="img", attrs=[("src", ...)]
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)


test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)
print(finder.images)

assert finder.images == [
    "/logo.png",                            # imagine obișnuită
    "poza.jpg",                             # tag scris cu majuscule
    "https://cdn.example.com/banner.webp",  # tag care se închide singur
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!")

# Rulare pe pagina reală
response = requests.get(BASE_URL, timeout=TIMEOUT)
finder = ImageFinder()
finder.feed(response.text)
print(len(finder.images), "imagini găsite")
for src in finder.images:
    print(src)
print("Verificare: <img apare de", response.text.lower().count("<img"), "ori")
time.sleep(1)


# ex 40

def page_fingerprint(url: str) -> str:
    """Returnează amprenta SHA-256 a conținutului paginii."""
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()


first = page_fingerprint(BASE_URL)
time.sleep(1)
second = page_fingerprint(BASE_URL)
print("Ex 40:", first)
print("Identice:", first == second)
# Diferă dacă pagina s-a schimbat între cereri (conținut dinamic: dată, oră,
# token CSRF, reclame, contor de vizitatori etc.).
time.sleep(1)

# ex 41
response = requests.get(BASE_URL, timeout=TIMEOUT)
with open("headers.json", "w", encoding="utf-8") as f:
    json.dump(dict(response.headers), f, indent=2)

with open("headers.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print("Ex 41:", loaded.get("Content-Type", "lipsește"))


# ex 42
print("Ex 42")
def resolve(hostname: str) -> str:
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return "IP negăsit"

ip_cybercor = resolve("cybercor.org")
print("Adresa IP pentru cybercor.org este:", ip_cybercor)


# ex 43
def cert_days_left(hostname: str) -> int:
    context = ssl.create_default_context()
    
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            
            not_after_str = cert["notAfter"]
            expire_timestamp = ssl.cert_time_to_seconds(not_after_str)
            
            now_timestamp = datetime.now(timezone.utc).timestamp()
            seconds_left = expire_timestamp - now_timestamp
            
            days = int(seconds_left // 86400)
            return days
days_remaining = cert_days_left("cybercor.org")
print(f"Certificatul SSL pentru cybercor.org mai este valabil {days_remaining} zile.")