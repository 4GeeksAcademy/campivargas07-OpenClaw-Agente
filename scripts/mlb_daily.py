#!/usr/bin/env python3
"""
MLB Daily Schedule — IPTV Edition v2
Clean daily MLB schedule for Carlos's IPTV business.
Channels focused on regional sports networks, national USA, and Mexican networks.
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request

# --- Config ---
CHAT_ID = "5969598217"
CDMX_OFFSET = timedelta(hours=-6)

# Team → Main regional channels (the ones IPTV users actually care about)
TEAM_REGIONAL = {
    "Arizona Diamondbacks": ["NBC Sports Arizona"],
    "Atlanta Braves": ["Bally Sports Southeast"],
    "Baltimore Orioles": ["MASN"],
    "Boston Red Sox": ["NESN"],
    "Chicago Cubs": ["Marquee"],
    "Chicago White Sox": ["NBC Sports Chicago"],
    "Cincinnati Reds": ["Bally Sports Ohio"],
    "Cleveland Guardians": ["Bally Sports Great Lakes"],
    "Colorado Rockies": ["Rockies.TV"],
    "Detroit Tigers": ["Bally Sports Detroit"],
    "Houston Astros": ["Space City Home Network"],
    "Kansas City Royals": ["Bally Sports Kansas City"],
    "Los Angeles Angels": ["Bally Sports West"],
    "Los Angeles Dodgers": ["Spectrum Sportsnet LA"],
    "Miami Marlins": ["Bally Sports Florida"],
    "Milwaukee Brewers": ["Bally Sports Wisconsin"],
    "Minnesota Twins": ["Bally Sports North"],
    "New York Mets": ["SNY"],
    "New York Yankees": ["YES"],
    "Oakland Athletics": ["NBC Sports California"],
    "Philadelphia Phillies": ["NBC Sports Philadelphia"],
    "Pittsburgh Pirates": ["SportsNet Pittsburgh"],
    "San Diego Padres": ["Bally Sports San Diego"],
    "San Francisco Giants": ["NBC Sports Bay Area"],
    "Seattle Mariners": ["ROOT Sports NW"],
    "St. Louis Cardinals": ["Bally Sports Midwest"],
    "Tampa Bay Rays": ["Bally Sports Sun"],
    "Texas Rangers": ["Bally Sports Southwest"],
    "Toronto Blue Jays": ["Sportsnet"],
    "Washington Nationals": ["MASN 2"],
}

NATIONAL_NETWORKS = {"ESPN", "ESPN2", "FOX", "FS1", "TBS", "MLB Network", "Apple TV+", "FOX Deportes"}
MX_NETWORKS = {"ESPN2 MX", "ESPN Deportes", "Fox Sports MX", "ESPN MX"}

# API returns "Bally Sports X" but many rebranded to "FanDuel Sports Network"
# Keep Bally names as they're more recognizable for IPTV

def get_token():
    """Get Telegram bot token from config."""
    with open("/root/.openclaw/openclaw.json") as f:
        config = json.load(f)
    return config.get("channels", {}).get("telegram", {}).get("botToken", "")

def fetch_games(date_str=None):
    """Fetch today's MLB schedule."""
    if date_str is None:
        date_str = (datetime.now(timezone.utc) + CDMX_OFFSET).strftime("%Y-%m-%d")

    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}&hydrate=broadcasts"
    with urlopen(url, timeout=30) as r:
        data = json.loads(r.read().decode())

    games = []
    for d in data.get("dates", []):
        games.extend(d.get("games", []))
    return games

def is_iptv_channel(name):
    """Check if a broadcast name is relevant for IPTV (not radio/streaming)."""
    name_lower = name.lower()
    # Skip radio
    if any(k in name_lower for k in ["fm", "am", "radio", "iheart", "audacy", "espn app"]):
        return False
    # Skip team-specific .TV streams
    if name_lower.endswith(".tv") and "mlb" not in name_lower:
        return False
    # Skip audio streams
    if any(k in name_lower for k in ["the fan", "talk ", "knbr", "wcco", "weei", "wjfk", "wlw", "wtmj", "kwfn", "ksfte"]):
        return False
    # Skip proxy "presented by" streams
    if "presented by" in name_lower:
        return False
    # Skip "A's Cast" type
    if "cast" in name_lower:
        return False
    return True

def get_channels(game):
    """Get relevant IPTV channels for a game."""
    home_team = game.get("teams", {}).get("home", {}).get("team", {}).get("name", "")
    away_team = game.get("teams", {}).get("away", {}).get("team", {}).get("name", "")
    
    channels = set()
    
    # 1. API broadcasts (filtered)
    for b in game.get("broadcasts", []):
        name = b.get("name", "")
        lang = b.get("language", "en")
        btype = b.get("type", "")
        if btype == "radio":
            continue
        if is_iptv_channel(name):
            channels.add(name)
        # Also grab Spanish channels (MX)
        if lang == "es" and name:
            channels.add(name)

    # 2. Regional channels from our map
    for team in [home_team, away_team]:
        if team in TEAM_REGIONAL:
            for c in TEAM_REGIONAL[team]:
                # Also add shortened versions
                channels.add(c)
                if "Bally Sports" in c:
                    short = c.replace("Bally Sports ", "Bally ")
                    channels.add(short)

    # 3. Normalize common names
    normalized = set()
    for c in channels:
        c2 = c.strip()
        # Standardize YES Network → YES
        if c2 == "YES Network":
            c2 = "YES"
        # Standardize ESPN/ESPN App → ESPN
        if "ESPN" in c2.upper() and ("App" in c2 or "App" in c2):
            c2 = "ESPN"
        # MLB.TV stays
        if c2.upper() == "MLB.TV" or c2 == "MLB.TV":
            c2 = "MLB.TV"
        # Space City Home Network → AT&T Sportsnet
        if "Space City" in c2:
            c2 = "AT&T Sportsnet"
        normalized.add(c2)

    # 4. Filter: keep only recognizable IPTV channels
    keep = []
    for c in normalized:
        # Check if it's a known major channel
        known = False
        test = c.lower()
        # Regional sports networks
        rsn_keywords = ["bally", "nbc sports", "nesn", "yes", "marquee", "sny", "masn",
                        "sportsnet", "spectrum sportsnet", "at&t", "root sports",
                        "space city", "sportsnet pittsburgh"]
        # National
        national_keywords = ["espn", "fox", "tbs", "mlb network", "apple tv", "fs1", "fox deportes", "fox sports"]
        # MX
        mx_keywords = ["espn2 mx", "espn deportes", "fox sports mx"]
        
        if any(k in test for k in rsn_keywords + national_keywords + mx_keywords):
            known = True
        elif test == "mlb.tv":
            known = True
            
        if known:
            keep.append(c)
    
    # If no channels found, default to MLB.TV
    if not keep:
        keep = ["MLB.TV"]
    
    return sorted(set(keep))

def fmt_time(dt):
    """Format datetime to CDMX time string."""
    return dt.strftime("%I:%M %p").lstrip("0").lower()

def build_message(games):
    """Build formatted Telegram message."""
    # Use the game date from the first game (more accurate)
    if games:
        gd = games[0].get("gameDate", "")
        try:
            today = datetime.fromisoformat(gd.replace("Z", "+00:00")) + CDMX_OFFSET
        except:
            today = datetime.now(timezone.utc) + CDMX_OFFSET
    else:
        today = datetime.now(timezone.utc) + CDMX_OFFSET
    
    dias_es = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    meses_es = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio",
                "Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    
    lines = []
    lines.append(f"⚾️  MLB — {dias_es[today.weekday()]} {today.day} de {meses_es[today.month-1]} {today.year}")
    lines.append("📍  Horarios CDMX (UTC-6)")
    lines.append("")
    
    # Sort games by time
    sorted_games = []
    for g in games:
        gd = g.get("gameDate", "")
        try:
            dt = datetime.fromisoformat(gd.replace("Z", "+00:00")) + CDMX_OFFSET
            sorted_games.append((dt, g))
        except:
            continue
    sorted_games.sort(key=lambda x: x[0])
    
    for dt, g in sorted_games:
        home = g.get("teams", {}).get("home", {}).get("team", {}).get("name", "?")
        away = g.get("teams", {}).get("away", {}).get("team", {}).get("name", "?")
        status = g.get("status", {}).get("detailedState", "")
        
        chs = get_channels(g)
        ch_str = " • ".join(chs)
        
        if status == "Final":
            hr = g.get("teams",{}).get("home",{}).get("score",0)
            ar = g.get("teams",{}).get("away",{}).get("score",0)
            lines.append(f"🏁  {away} {ar}—{hr} {home}    {ch_str}")
        else:
            t = fmt_time(dt)
            lines.append(f"🕐  {t:>8}   {away} @ {home}")
            lines.append(f"         📺 {ch_str}")
    
    # Stats
    total = len(games)
    final = sum(1 for _,g in sorted_games if g.get("status",{}).get("detailedState")=="Final")
    upcoming = total - final
    
    lines.append("")
    lines.append(f"📊 {upcoming} juegos programados · {final} finalizados")
    
    return "\n".join(lines)

def send_telegram(text):
    """Send message via Telegram Bot API."""
    token = get_token()
    payload = json.dumps({
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }).encode()
    
    req = Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urlopen(req, timeout=30) as r:
        result = json.loads(r.read().decode())
    return result.get("ok", False)

def main():
    now_cdmx = datetime.now(timezone.utc) + CDMX_OFFSET
    today_str = now_cdmx.strftime("%Y-%m-%d")
    
    # If it's late (past 8 PM), fetch tomorrow's games
    if now_cdmx.hour >= 20:
        tomorrow = (now_cdmx + timedelta(days=1)).strftime("%Y-%m-%d")
        games = fetch_games(tomorrow)
        print(f"Late hour, fetching tomorrow ({tomorrow})", file=sys.stderr)
    else:
        games = fetch_games(today_str)
        print(f"Fetching today ({today_str})", file=sys.stderr)
        if not games:
            tomorrow = (now_cdmx + timedelta(days=1)).strftime("%Y-%m-%d")
            games = fetch_games(tomorrow)
            print(f"No games today, trying {tomorrow}", file=sys.stderr)
    
    if not games:
        msg = "⚾️ No hay juegos de MLB programados para los próximos días."
        print(msg, file=sys.stderr)
        send_telegram(msg)
        return
    
    msg = build_message(games)
    print(f"Message: {len(msg)} chars", file=sys.stderr)
    
    ok = send_telegram(msg)
    if ok:
        print("✅ Sent!", file=sys.stderr)
    else:
        print("❌ Failed!", file=sys.stderr)
        with open("/root/tmp/mlb_error.txt", "w") as f:
            f.write(msg)
        sys.exit(1)

if __name__ == "__main__":
    main()