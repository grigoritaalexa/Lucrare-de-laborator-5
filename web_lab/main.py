# Laborator: funcții, metode și importuri pe web
# Student: Grigorița Alexandra

import csv
import argparse
from datetime import datetime

#ex 44 si 45
print("Ex 44 & 45")
import webtools
from webtools import get_title, security_headers, DEFAULT_HEADERS, check_paths, site_report

#ex 48
print("Ex 48")
parser = argparse.ArgumentParser(description="Instrument de analiză și raportare site-uri web.")
parser.add_argument("url", nargs="?", default="https://cybercor.org", help="URL-ul site-ului țintă")
args = parser.parse_args()

target_url = args.url

print(f"--- Rulare main.py pentru ținta: {target_url} ---")

# Demonstrație Exercițiul 44 & 47
print("User-Agent folosit (DEFAULT_HEADERS):", DEFAULT_HEADERS)
page_res = webtools.fetch(target_url)
print("Titlul paginii prin webtools:", get_title(page_res.text))

#ex 49
print("Ex 49")
print("Generare raport CSV (Exercițiul 49)")
paths_to_check = ["/", "/robots.txt", "/sitemap.xml", "/admin"]
check_results = check_paths(target_url, paths_to_check)

with open("report.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["path", "status", "checked_at"])
    
    now_iso = datetime.now().isoformat()
    for path, status in check_results.items():
        writer.writerow([path, status, now_iso])

print("Rezultatele verificării căilor au fost salvate în 'report.csv'.")

#ex 50
print("Ex 50")
print("Rulare proiect final (Exercițiul 50) ")
site_report(target_url)