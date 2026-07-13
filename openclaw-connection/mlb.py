#!/usr/bin/env python3
"""MLB Daily Schedule — via ESPN API
Uso: python3 mlb.py [YYYYMMDD]
Si no se pasa fecha, muestra la de hoy
"""
import sys, json, urllib.request
from datetime import datetime, timezone

DATE = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).strftime("%Y%m%d")

url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={DATE}"
req = urllib.request.urlopen(url)
data = json.loads(req.read())
events = data.get("events", [])

print("=" * 45)
print(f"  MLB Schedule - {DATE}")
print("=" * 45)
print()

if not events:
    print("No games scheduled for this date.")
    print("(All-Star break or offseason)")
    sys.exit(0)

for i, e in enumerate(events, 1):
    name = e.get("name", "")
    comps = e.get("competitions", [{}])[0]
    venue = comps.get("venue", {}).get("fullName", "N/A")
    status = comps.get("status", {}).get("type", {}).get("description", "")
    teams = comps.get("competitors", [])

    t1 = teams[0].get("team", {}).get("displayName", "")
    t2 = teams[1].get("team", {}).get("displayName", "")
    r1 = teams[0].get("score", "-")
    r2 = teams[1].get("score", "-")

    rec1 = teams[0].get("records", [{}])
    rec2 = teams[1].get("records", [{}])
    wl1 = rec1[0].get("summary", "") if rec1 else ""
    wl2 = rec2[0].get("summary", "") if rec2 else ""

    odds = comps.get("odds", [{}])
    spread = odds[0].get("details", "") if odds else ""
    ou = odds[0].get("overUnder", "") if odds else ""

    dt = comps.get("date", e.get("date", ""))
    try:
        game_time = datetime.fromisoformat(dt.replace("Z", "+00:00")).strftime("%I:%M %p ET")
    except:
        game_time = dt

    print(f"{i}. {name}")
    print(f"   {t1:25s} ({wl1:10s}) vs {t2:25s} ({wl2:10s})")
    print(f"   Venue: {venue}")
    print(f"   Time: {game_time}  |  Score: {r1} - {r2}  |  {status}")
    if spread or ou:
        print(f"   Odds: {spread}  O/U {ou}")
    print()