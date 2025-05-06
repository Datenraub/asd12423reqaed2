import requests
import time
import os
import random
import sys
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init()
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = RESET = ''
    class Style:
        BRIGHT = RESET_ALL = ''

TOKEN_FILE = "tokens.txt"
LOG_FILE = "log.txt"

def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(Fore.CYAN + "=" * 60)
    print(Style.BRIGHT + "🤖  DISCORD ULTIMATE TOOLKIT | Für eigene Zwecke  ")
    print("=" * 60 + Style.RESET_ALL + Fore.RESET)

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

def spam_message(token, channel_id, message):
    headers = get_headers(token)
    payload = {"content": message}
    r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=payload)
    timestamp = datetime.now().strftime('%H:%M:%S')
    if r.status_code == 200:
        print(Fore.GREEN + f"[{timestamp}] ✅ Gesendet: {message[:20]}..." + Fore.RESET)
        log(f"[SUCCESS] Token {token[:8]}... -> Channel {channel_id}: {message}")
    elif r.status_code == 429:
        retry_after = r.json().get("retry_after", 1)
        print(Fore.YELLOW + f"[{timestamp}] ⚠️ Rate Limit! Warte {retry_after}s..." + Fore.RESET)
        time.sleep(retry_after)
    else:
        print(Fore.RED + f"[{timestamp}] ❌ Fehler {r.status_code}: {r.text}" + Fore.RESET)
        log(f"[FAIL] {r.status_code} -> {r.text}")

def spam_loop(token, channels, message, count, delay, randomize=False):
    for i in range(count):
        target = random.choice(channels) if randomize else channels[i % len(channels)]
        spam_message(token, target, message)
        time.sleep(delay)

def spam_from_file(token, channels, filepath, count, delay):
    if not os.path.exists(filepath):
        print("❌ Datei nicht gefunden.")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    for i in range(count):
        msg = random.choice(lines)
        chan = random.choice(channels)
        spam_message(token, chan, msg)
        time.sleep(delay)

def main():
    while True:
        banner()
        if not os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "w") as f: pass
        token = input("🔑 Token eingeben (wird gespeichert): ").strip()
        with open(TOKEN_FILE, "a") as f:
            f.write(token + "\n")
        if not validate_token(token):
            print(Fore.RED + "❌ Token ungültig!" + Fore.RESET)
            input("↩️ Enter zum Neuversuch...")
            continue

        chans = input("📥 Channel-IDs kommasepariert: ").strip().split(",")
        chans = [c.strip() for c in chans if c.strip()]
        if not all(validate_channel(token, c) for c in chans):
            print(Fore.RED + "❌ Mind. 1 Channel ungültig oder kein Zugriff!" + Fore.RESET)
            input("↩️ Enter zum Neuversuch...")
            continue

        banner()
        print("1️⃣ Nachricht mehrfach senden")
        print("2️⃣ Nachrichten aus Datei random spammen")
        print("3️⃣ Logs anzeigen")
        print("4️⃣ Exit")
        choice = input("👉 Auswahl: ").strip()

        if choice == "1":
            msg = input("📝 Nachricht: ").strip()
            count = int(input("🔁 Wiederholungen: "))
            delay = float(input("⏱️ Delay (Sekunden): "))
            spam_loop(token, chans, msg, count, delay, randomize=True)
        elif choice == "2":
            file = input("📂 Pfad zur Textdatei: ").strip()
            count = int(input("🔁 Wiederholungen: "))
            delay = float(input("⏱️ Delay (Sekunden): "))
            spam_from_file(token, chans, file, count, delay)
        elif choice == "3":
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    print(Fore.YELLOW + f.read() + Fore.RESET)
            else:
                print("Keine Logs vorhanden.")
            input("↩️ Zurück...")
        elif choice == "4":
            print("👋 Bis bald, Bruder.")
            break
        else:
            print("❌ Ungültige Auswahl!")

if __name__ == "__main__":
    main()
