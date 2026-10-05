# Laborator: funcții, metode și importuri pe web
# Student: Grigorița Alexandra

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Ex 9
print("Ex 9")
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("status_code:", response.status_code) #Atribut
print("ok:", response.ok) #Atribut
print("url:", response.url) #Atribut
print("encoding:", response.encoding) #Atribut

# Ex 10  
print("Ex 10")
response.raise_for_status()
invalid_url = ECHO_URL + "/status/404"

try:
    bad_response = requests.get(invalid_url, timeout=TIMEOUT)
    bad_response.raise_for_status()
except requests.HTTPError as error:
    print(f"Eroare HTTP prinsa cu succes! Pagina nu a fost gasita: {error}")

time.sleep(1)

# Ex 11
print("Ex 11")
for name, value in response.headers.items():
    print(f"{name}: {value}")

# Ex 12
print("Ex 12")
print("Server:", response.headers.get("Server", "lipsește"))
print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("content-type (litere mici):", response.headers.get("content-type", "lipsește"))
# Observație: funcționează și cu litere mici, deoarece response.headers
# este un dicționar insensibil la majuscule (CaseInsensitiveDict).

#Ex 13
print("Ex 13")
count = response.text.lower().count("cyber")
print("Cuvântul 'cyber' apare de", count, "ori")
# Putem înlănțui pentru că .lower() returnează un șir nou (str),
# iar un str are la rândul lui metoda .count().

# Ex 14
print("Ex 14")
html = response.text
start = html.find("<title>") + len("<title>")
end = html.find("</title>")
title = html[start:end].strip()
print("Titlu:", title)

# Ex 15
print("Ex 15")
lines = html.splitlines()
print("Număr de linii:", len(lines))
print("Lungimea celei mai lungi linii:", len(max(lines, key=len)))

# Ex 16
print("Ex 16")
if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")

time.sleep(1)

# Ex 17
print("Ex 17")
r = requests.get("http://cybercor.org", timeout=TIMEOUT)
for step in r.history:
    print(step.status_code, step.url)
print("URL final:", r.url)

time.sleep(1)

# Ex 18
print("Ex 18")
head_resp = requests.head(BASE_URL, timeout=TIMEOUT)
time.sleep(1)
get_resp = requests.get(BASE_URL, timeout=TIMEOUT)
print("HEAD:", len(head_resp.content), "octeți")
print("GET: ", len(get_resp.content), "octeți")
# HEAD cere doar antetele, serverul nu trimite corpul paginii (0 octeți).
# GET returnează antetele ȘI corpul (codul HTML).

time.sleep(1)

# Ex 19
print("Ex 19")
if len(response.cookies) == 0:
    print("Niciun cookie setat")
else:
    for cookie in response.cookies:
        print(cookie.name, cookie.secure)

# Ex 20
print("Ex 20")
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-<numele vostru>"})
echo = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print(echo.text)  # trebuie să conțină User-Agent: WebLab-...


