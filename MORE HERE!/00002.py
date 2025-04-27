import requests
from bs4 import BeautifulSoup
import csv
import os
import time
from tqdm import tqdm
import threading

OUTPUT_FOLDER = "output_apps"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Storage for apps
apps = []

# Scraping Microsoft Store
def scrape_microsoft():
    url = "https://www.microsoft.com/en-us/store/most-popular/apps/pc"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")

    for link in tqdm(soup.find_all('a', href=True), desc="Scraping Microsoft Store"):
        href = link['href']
        if "/p/" in href:
            app_name = link.get_text(strip=True)
            full_link = f"https://www.microsoft.com{href}"
            if app_name:
                apps.append({
                    "name": app_name,
                    "category": "App (Microsoft Store)",
                    "link": full_link,
                    "source": "Microsoft Store"
                })

# Scraping PCMag
def scrape_pcmag():
    url = "https://www.pcmag.com/picks/best-apps-in-the-windows-11-store"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")

    for section in tqdm(soup.find_all('a', href=True), desc="Scraping PCMag"):
        href = section['href']
        if href.startswith("http") and "pcmag.com" not in href:
            app_name = section.get_text(strip=True)
            if app_name:
                apps.append({
                    "name": app_name,
                    "category": "App (PCMag)",
                    "link": href,
                    "source": "PCMag"
                })

# Save CSV
def save_csv():
    with open(os.path.join(OUTPUT_FOLDER, "apps.csv"), "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "category", "link", "source"])
        writer.writeheader()
        for app in apps:
            writer.writerow(app)

# Save XML
def save_xml():
    with open(os.path.join(OUTPUT_FOLDER, "apps.xml"), "w", encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<apps>\n')
        for app in apps:
            f.write(f'  <app>\n')
            f.write(f'    <name>{app["name"]}</name>\n')
            f.write(f'    <category>{app["category"]}</category>\n')
            f.write(f'    <link>{app["link"]}</link>\n')
            f.write(f'    <source>{app["source"]}</source>\n')
            f.write(f'  </app>\n')
        f.write('</apps>')

# Save HTML
def save_html():
    with open(os.path.join(OUTPUT_FOLDER, "apps.html"), "w", encoding='utf-8') as f:
        f.write('<html><head><title>Apps List</title></head><body>\n')
        f.write('<h1>Collected Apps</h1>\n<table border="1">\n')
        f.write('<tr><th>Name</th><th>Category</th><th>Link</th><th>Source</th></tr>\n')
        for app in apps:
            f.write(f'<tr><td>{app["name"]}</td><td>{app["category"]}</td><td><a href="{app["link"]}">Link</a></td><td>{app["source"]}</td></tr>\n')
        f.write('</table>\n</body></html>')

# Main runner
def main():
    threads = []
    
    # Create threads
    t1 = threading.Thread(target=scrape_microsoft)
    t2 = threading.Thread(target=scrape_pcmag)
    
    t1.start()
    t2.start()
    
    threads.append(t1)
    threads.append(t2)
    
    for t in threads:
        t.join()

    # Save results
    save_csv()
    save_xml()
    save_html()
    print(f"\n✅ Completed! Saved CSV, XML, HTML in '{OUTPUT_FOLDER}'.")

# Delay 10 seconds (task start delay)
print("⏳ Waiting 10 seconds before scraping...")
time.sleep(10)

# Start the main scraper
start_time = time.time()
main()
elapsed = time.time() - start_time

# Check against emergency stop
if elapsed > 65:
    print("\n❌ Emergency stop! Task took too long!")
else:
    print(f"\n✅ Finished in {elapsed:.2f} seconds! Within limit.")

