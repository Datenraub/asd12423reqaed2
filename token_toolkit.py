import requests
import time
import os
import random
import sys
from datetime import datetime

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print("=" * 60)
    print("🤖  DISCORD TOKEN TOOLKIT  |  Für EIGENE Server (SAFE)  ")
    print("=" * 60)

def get_headers(token):
    return {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

def validate_token(token):
    r = requests.get("https://discord.com/api/v9/users/@me", headers=get_headers(token))
    return r.status_code == 200

def validate_channel(token, channel_id):
    r = requests.get(f"https://discord.com/api/v9/channels/{channel_id}", headers=get_headers(token))
    return r.status_code == 200

def spam_fixed(token, channel_id, message, count, delay):
    headers = get_headers(token)
    for i in range(count):
        payload = {"content": message}
        r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=payload)
        timestamp = datetime.now().strftime('%H:%M:%S')
        if r.status_code == 200:
            print(f"[{timestamp}] ({i+1}/{count}) ✅ Gesendet")
        elif r.status_code == 429:
            retry_after = r.json().get("retry_after", 1)
            print(f"[{timestamp}] ⚠️ Rate Limit! Warte {retry_after}s...")
            time.sleep(retry_after)
        else:
            print(f"[{timestamp}] ❌ Fehler {r.status_code}: {r.text}")
        time.sleep(delay)

def spam_from_file(token, channel_id, filepath, count, delay):
    if not os.path.exists(filepath):
        print("❌ Datei nicht gefunden.")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    for i in range(count):
        message = random.choice(lines)
        spam_fixed(token, channel_id, message, 1, delay)

def main():
    while True:
        banner()
        token = input("🔑 Gib deinen Token ein: ").strip()
        if not validate_token(token):
            print("❌ Ungültiger Token!")
            input("↩️ Enter zum Neuversuch...")
            continue

        channel_id = input("🧩 Channel-ID eingeben: ").strip()
        if not validate_channel(token, channel_id):
            print("❌ Channel existiert nicht oder keine Rechte.")
            input("↩️ Enter zum Neuversuch...")
            continue

        banner()
        print("1️⃣ Nachricht mehrfach senden")
        print("2️⃣ Nachrichten aus Datei random spammen")
        print("3️⃣ Exit")
        auswahl = input("👉 Auswahl: ").strip()

        if auswahl == "1":
            message = input("✉️ Nachricht: ").strip()
            count = int(input("🔁 Wie oft? "))
            delay = float(input("⏱️ Delay (Sekunden): "))
            spam_fixed(token, channel_id, message, count, delay)
        elif auswahl == "2":
            filepath = input("📂 Pfad zur Textdatei (.txt): ").strip()
            count = int(input("🔁 Wie oft? "))
            delay = float(input("⏱️ Delay (Sekunden): "))
            spam_from_file(token, channel_id, filepath, count, delay)
        elif auswahl == "3":
            print("👋 Bis bald, Bruder.")
            sys.exit()
        else:
            print("❌ Ungültige Auswahl!")

        input("↩️ Enter für Hauptmenü...")

if __name__ == "__main__":
    main()
