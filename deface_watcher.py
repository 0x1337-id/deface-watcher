import requests
import hashlib
import os
import time
from datetime import datetime

def get_page_hash(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text.encode("utf-8")
        return hashlib.md5(content).hexdigest(), response.text
    except Exception as e:
        print(f"[!] Error accessing {url}: {e}")
        return None, None

def save_baseline(url, content):
    with open("baseline.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("[✓] Baseline saved as baseline.html")

def load_baseline_hash():
    if not os.path.exists("baseline.html"):
        return None
    with open("baseline.html", "r", encoding="utf-8") as f:
        content = f.read().encode("utf-8")
        return hashlib.md5(content).hexdigest()

def monitor(url):
    print(f"[~] Checking website: {url}")
    current_hash, current_content = get_page_hash(url)
    if current_hash is None:
        return

    baseline_hash = load_baseline_hash()
    if baseline_hash is None:
        print("[!] Baseline not found. Creating one now...")
        save_baseline(url, current_content)
        return

    if current_hash != baseline_hash:
        print(f"[!] WARNING: Website content might have changed! ({datetime.now()})")
        with open("alert_snapshot.html", "w", encoding="utf-8") as f:
            f.write(current_content)
        print("[!] Snapshot saved to alert_snapshot.html")
    else:
        print("[✓] Website content is unchanged.")

if __name__ == "__main__":
    target_url = input("Masukkan URL target (cth: https://example.com): ").strip()
    monitor(target_url)
  
