import os
import json
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FD_API_KEY")
TEAM_ID = 66  # Manchester United (football-data.org)
LIMIT = 10

if not API_KEY:
    raise RuntimeError("FD_API_KEY environment variable not set")

URL = f"https://api.football-data.org/v4/teams/{TEAM_ID}/matches"
PARAMS = {
    "status": "FINISHED",
    "limit": LIMIT,
}

headers = {"X-Auth-Token": API_KEY}

resp = requests.get(URL, headers=headers, params=PARAMS, timeout=20)
resp.raise_for_status()
data = resp.json()

matches = data.get("matches", [])

if not matches:
    print("No matches returned.")
    raise SystemExit(0)

# IMPORTANT: ensure most recent match is first
matches.sort(key=lambda m: m.get("utcDate", ""), reverse=True)

print(f"\nMost recent FINISHED matches (newest → oldest), limit={LIMIT}:")
for m in matches:
    date = (m.get("utcDate") or "")[:10]
    home = m["homeTeam"]["name"]
    away = m["awayTeam"]["name"]
    ft_home = m["score"]["fullTime"]["home"]
    ft_away = m["score"]["fullTime"]["away"]
    print(f"{date} | {home} {ft_home}-{ft_away} {away}")

streak = 0
first_break_reason = None

for m in matches:
    is_home = (m["homeTeam"]["id"] == TEAM_ID)

    ft_home = m["score"]["fullTime"]["home"]
    ft_away = m["score"]["fullTime"]["away"]

    # Defensive skip (shouldn't happen for FINISHED, but safe)
    if ft_home is None or ft_away is None:
        continue

    gf = ft_home if is_home else ft_away
    ga = ft_away if is_home else ft_home

    if gf > ga:
        streak += 1
    else:
        if gf == ga:
            first_break_reason = "draw"
        else:
            first_break_reason = "loss"
        break

print(f"\nManchester United current win streak: {streak}")
if first_break_reason:
    print(f"Streak broke due to a {first_break_reason} in the most recent sequence.")

if streak == 0:
    status = "😂😂😂"
    color = "lightgrey"
elif streak < 3:
    status = "🥶🥶🥶"
    color = "orange"
else:
    status = "🔥🔥🔥 AMORIMS RED ARMYYY"
    color = "red"

badge = {
    "schemaVersion": 1,
    "label": "Man Utd win streak",
    "message": f"{streak} games — {status}",
    "color": color,
}

os.makedirs("badges", exist_ok=True)
with open("badges/mu-streak.json", "w", encoding="utf-8") as f:
    json.dump(badge, f, indent=2)

print("\nBadge JSON written to badges/mu-streak.json\n")
