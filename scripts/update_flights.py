#!/usr/bin/env python3
"""Update the live flight radar section of README.md.

Fetches one snapshot from OpenSky Network's free /states/all endpoint,
computes headline stats, and rewrites the block between the FLIGHT-DATA
markers in README.md. Driven by .github/workflows/radar.yml on a 3-hour
cron. Stdlib only — no runtime dependencies.

OpenSky schema reference:
    https://openskynetwork.github.io/opensky-api/rest.html#all-state-vectors
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple, Optional


# Config

OPENSKY_URL = "https://opensky-network.org/api/states/all"
USER_AGENT = "frankie-aerocloud-readme/2.0 (+github actions)"
HTTP_TIMEOUT_SECONDS = 45
TOP_COUNTRIES_LIMIT = 8
DASHBOARD_INNER_WIDTH = 68

MARKER_START = "<!-- FLIGHT-DATA:START -->"
MARKER_END = "<!-- FLIGHT-DATA:END -->"

README = Path(__file__).resolve().parent.parent / "README.md"

# Daily-rotation featured-hub roster. (display name, ICAO, IATA, one-liner)
FEATURED_AIRPORTS = [
    ("Atlanta",           "KATL", "ATL", "Busiest airport on Earth - 100M+ passengers a year pass through."),
    ("Dubai",             "OMDB", "DXB", "World's #1 for international traffic. An A380 lands here every few minutes."),
    ("Dallas/Fort Worth", "KDFW", "DFW", "Bigger than the island of Manhattan - five parallel runways."),
    ("London Heathrow",   "EGLL", "LHR", "Two runways, ~1,300 movements a day. Slot coordination as a sport."),
    ("Tokyo Haneda",      "RJTT", "HND", "Famously punctual - average delay measured in seconds."),
    ("Paris CDG",         "LFPG", "CDG", "Europe's second-busiest. Terminal 1 is a brutalist concrete donut."),
    ("Chicago O'Hare",    "KORD", "ORD", "Eight runways. The original mega-hub."),
    ("Los Angeles",       "KLAX", "LAX", "The Pacific Rim's gateway. 24/7, 365."),
    ("Singapore Changi",  "WSSS", "SIN", "Voted world's best airport more times than anyone can count."),
    ("Amsterdam Schiphol","EHAM", "AMS", "One terminal, six runways, an entire city's worth of bicycles."),
    ("Hong Kong",         "VHHH", "HKG", "Built on a man-made island. The cargo capital of the world."),
    ("Frankfurt",         "EDDF", "FRA", "Europe's freight king and Lufthansa's fortress hub."),
]


# Typed schema

class StateVector(NamedTuple):
    """One aircraft snapshot. Field order matches OpenSky's /states/all schema.

    Only the first 17 documented positions are mapped so that optional
    trailing fields (e.g. `category` on newer API revisions) don't break us.
    """
    icao24: str                       # Unique ICAO 24-bit transponder address.
    callsign: Optional[str]           # Callsign (up to 8 chars).
    origin_country: str               # Country inferred from the ICAO prefix.
    time_position: Optional[int]      # Last position update (unix epoch s).
    last_contact: int                 # Last update of any kind (unix epoch s).
    longitude: Optional[float]        # WGS-84 longitude (degrees).
    latitude: Optional[float]         # WGS-84 latitude (degrees).
    baro_altitude: Optional[float]    # Barometric altitude (metres).
    on_ground: bool                   # True if the aircraft is on the ground.
    velocity: Optional[float]         # Ground velocity (m/s).
    true_track: Optional[float]       # Track angle, true north clockwise (deg).
    vertical_rate: Optional[float]    # Vertical rate (m/s, +ve = climbing).
    sensors: Optional[list]           # IDs of contributing sensors.
    geo_altitude: Optional[float]     # Geometric altitude (metres).
    squawk: Optional[str]             # Transponder code.
    spi: bool                         # Special-purpose indicator flag.
    position_source: int              # 0=ADS-B, 1=ASTERIX, 2=MLAT, 3=FLARM.

    @classmethod
    def from_raw(cls, raw):
        return cls(*raw[:17])


# Fetch + minimal schema check

class OpenSkyError(Exception):
    """Anything went wrong talking to OpenSky (network, parse, or schema)."""


def fetch_states() -> dict:
    req = urllib.request.Request(OPENSKY_URL, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise OpenSkyError(f"{type(exc).__name__}: {exc}") from exc

    # Reject malformed responses before they reach the renderer.
    if not isinstance(payload, dict) or "states" not in payload:
        raise OpenSkyError(f"unexpected response shape: {type(payload).__name__}")
    states = payload["states"]
    if states and (not isinstance(states[0], list) or len(states[0]) < 17):
        raise OpenSkyError("malformed state record")
    return payload


# Rendering

def m_to_ft(m):  return m * 3.28084
def mps_to_kts(m): return m * 1.94384


class Summary(NamedTuple):
    """Pre-computed numbers needed to render the dashboard + countries table."""
    total: int
    airborne: int
    grounded: int
    avg_alt_ft: float
    avg_spd_kts: float
    highest: Optional[StateVector]
    fastest: Optional[StateVector]
    top_countries: list


def _summarise(states: list) -> Summary:
    airborne   = [s for s in states if not s.on_ground]
    altitudes  = [s.baro_altitude for s in airborne if s.baro_altitude is not None]
    velocities = [s.velocity      for s in airborne if s.velocity      is not None]
    return Summary(
        total         = len(states),
        airborne      = len(airborne),
        grounded      = len(states) - len(airborne),
        avg_alt_ft    = m_to_ft(sum(altitudes) / len(altitudes))     if altitudes  else 0,
        avg_spd_kts   = mps_to_kts(sum(velocities) / len(velocities)) if velocities else 0,
        highest       = max((s for s in airborne if s.baro_altitude is not None),
                            key=lambda s: s.baro_altitude, default=None),
        fastest       = max((s for s in airborne if s.velocity is not None),
                            key=lambda s: s.velocity, default=None),
        top_countries = Counter(
            s.origin_country for s in airborne if s.origin_country
        ).most_common(TOP_COUNTRIES_LIMIT),
    )


def _flight_label(s: StateVector) -> str:
    """Best human-readable label for a flight: callsign, else ICAO id, else 'unknown'."""
    return (s.callsign or "").strip() or s.icao24 or "unknown"


def _row(label: str, value: str, width: int = DASHBOARD_INNER_WIDTH) -> str:
    """One dashboard row: ║ label ........ value ║, padded to width."""
    dots = max(2, width - len(label) - len(value) - 2)
    return f"║ {label} {'.' * dots} {value} ║"


def _render_dashboard(s: Summary, timestamp: str) -> list:
    highest_cs = _flight_label(s.highest)                            if s.highest else "n/a"
    highest_ft = f"{m_to_ft(s.highest.baro_altitude):,.0f} ft"        if s.highest else "n/a"
    fastest_cs = _flight_label(s.fastest)                            if s.fastest else "n/a"
    fastest_kt = f"{mps_to_kts(s.fastest.velocity):,.0f} kts"         if s.fastest else "n/a"
    return [
        "```",
        "╔══════════════════════════════════════════════════════════════════════╗",
        "║" + "✈   L I V E   G L O B A L   F L I G H T   R A D A R   ✈".center(70) + "║",
        "║" + timestamp.center(70) + "║",
        "╠══════════════════════════════════════════════════════════════════════╣",
        _row("Aircraft tracked worldwide",          f"{s.total:,}"),
        _row("  └── currently airborne",             f"{s.airborne:,}"),
        _row("  └── on the ground (taxi / parked)", f"{s.grounded:,}"),
        "║" + " " * 70 + "║",
        _row("Average cruise altitude",              f"{s.avg_alt_ft:,.0f} ft"),
        _row("Average ground speed",                 f"{s.avg_spd_kts:,.0f} kts"),
        _row(f"Highest flight ({highest_cs})",       highest_ft),
        _row(f"Fastest flight ({fastest_cs})",       fastest_kt),
        "╚══════════════════════════════════════════════════════════════════════╝",
        "```",
    ]


def _render_countries_table(top_countries: list) -> list:
    header = [
        "### 🌍  Busiest Skies Right Now",
        "",
        "> Top countries by aircraft currently airborne.",
        "",
        "| # | Country of registration | Aircraft aloft |",
        "|:---:|:---|---:|",
    ]
    rows = [f"| {i} | {country} | {count:,} |"
            for i, (country, count) in enumerate(top_countries, 1)]
    return header + rows


def _render_featured_hub() -> list:
    day = datetime.now(timezone.utc).timetuple().tm_yday
    city, _icao, iata, fact = FEATURED_AIRPORTS[day % len(FEATURED_AIRPORTS)]
    return [
        f"### 🛫  Today's Featured Hub — `{iata}` · {city}",
        "",
        f"> _{fact}_",
        "",
        "> Hubs at this scale are exactly where AeroCloud's "
        "**Airport Operations System** and **Passenger Flow Monitoring** "
        "earn their keep — every flight here is a small symphony of stands, "
        "gates, baggage belts, immigration desks, and people.",
    ]


def _render_footer(timestamp: str) -> str:
    return (
        f"<sub>📡 Last transmission: <b>{timestamp}</b> &nbsp;·&nbsp; "
        f"Source: <a href=\"https://opensky-network.org\">OpenSky Network</a> "
        f"(free, no API key) &nbsp;·&nbsp; Refreshed every 3 h by GitHub Actions.</sub>"
    )


def build_section(data: dict) -> str:
    """Build the markdown that lives between the FLIGHT-DATA markers."""
    states    = [StateVector.from_raw(s) for s in (data.get("states") or [])]
    summary   = _summarise(states)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    parts = [
        *_render_dashboard(summary, timestamp),
        "",
        *_render_countries_table(summary.top_countries),
        "",
        *_render_featured_hub(),
        "",
        _render_footer(timestamp),
    ]
    return "\n".join(parts)


def replace_block(text: str, payload: str) -> str:
    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.DOTALL)
    new, n = pattern.subn(f"{MARKER_START}\n{payload}\n{MARKER_END}", text)
    if n == 0:
        raise RuntimeError(f"Markers not found in README.md: {MARKER_START} / {MARKER_END}")
    return new


# Entrypoint

def log(msg):
    print(f"radar | {msg}", file=sys.stderr, flush=True)


def main() -> int:
    try:
        data = fetch_states()
    except OpenSkyError as exc:
        log(f"OpenSky fetch failed ({exc}); leaving previous snapshot in place.")
        return 0  # transient upstream blip — keep the last good README

    states_count = len(data.get("states") or [])
    section = build_section(data)
    text = README.read_text(encoding="utf-8")
    updated = replace_block(text, section)
    if updated != text:
        README.write_text(updated, encoding="utf-8")
        log(f"updated README ({states_count:,} states processed)")
    else:
        log(f"no changes ({states_count:,} states processed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
