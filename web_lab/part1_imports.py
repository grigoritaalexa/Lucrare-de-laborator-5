# Laborator: funcții, metode și importuri pe web
# Student: Grigorița Alexandra
import urllib.request
import ssl
import certifi
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


#ex1
import requests
import urllib.request

print(" Ex 1 Versiunea requests:", requests.__version__)

#  requests este o bibliotecă externă de aceea trebuie instalată cu pip install requests iar urllib face parte din biblioteca standard, care este inclusă în Python.

#ex2
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex 2 (import requests):", response.status_code)

from requests import get

response = get(BASE_URL, timeout=TIMEOUT)
print("Ex 2 (from requests import get):", response.status_code)

# Avantaj "import requests" este că se vede mereu de unde vine funcția și nu există conflicte de nume cu alte funcții numite get.
# Avantaj "from requests import get": codul este mai scurt, nu repeți prefixul.

# ex3
import requests as rq

response = rq.get(BASE_URL, timeout=TIMEOUT)
print("Ex 3 (alias rq):", response.status_code)

# Un alias ajută când numele e lung și îl scrii des (ex: import numpy as np).
# Un alias încurcă când numele ales nu spune nimic (ex: rq, x),

# ex4
print("Ex 4")

import urllib.request
import ssl

# Setăm un User-Agent pentru a preveni blocarea cererilor de către server
req = urllib.request.Request(
    BASE_URL, 
    headers={"User-Agent": "Mozilla/5.0 (compatible; TP_laborator)"}
)

# Ignorăm verificarea strictă SSL dacă certificatul serverului creează probleme
context = ssl._create_unverified_context()

try:
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=context) as response:
        status = response.status
        body_bytes = response.read()
        body_str = body_bytes.decode("utf-8")
        
        print("Status urllib:", status)
        print("Primele 200 de caractere:", body_str[:200])
except Exception as e:
    print(f"Eroare la conectare cu urllib: {e}")


    

#ex5
print(dir(requests))

# Exemple alese (verificați în rezultatul vostru):
# - get      -> funcție
# - Session  -> clasă
# - exceptions -> modul (submodul al pachetului requests)

# ex6
help(requests.get)

# Parametrul care setează timpul maxim de așteptare este "timeout".
response = requests.get(BASE_URL, timeout=5)
print("Ex 6:", response.status_code)

#ex7
import time

start = time.perf_counter()
response = requests.get(BASE_URL, timeout=TIMEOUT)
end = time.perf_counter()

print(f"perf_counter: {end - start:.3f} s")
print(f"response.elapsed: {response.elapsed.total_seconds():.3f} s")
# perf_counter măsoară tot (inclusiv conectarea și citirea corpului),
# response.elapsed măsoară doar până la primirea antetelor.

# ex8
try:
    import bs4
    print("bs4 este instalat, versiunea:", bs4.__version__)
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")
