<div align="center">

```sh
╔══════════════════════════════════════════════════════════════════════╗
║  BOARDING PASS                          AEROCLOUD SYSTEMS AIRLINES   ║
╠══════════════════════════════════════════════════════════════════════╣
║  PASSENGER            FROM           TO               FLIGHT    SEAT ║
║  FRANCESCO WANG       DEV            PRODUCTION       AC2026    1A   ║
╠══════════════════════════════════════════════════════════════════════╣
║  GATE         BOARDING               CLASS            STATUS         ║
║  3            ALWAYS BOARDING        BUSINESS         ON TIME        ║
╠══════════════════════════════════════════════════════════════════════╣
║  ||| |||| | || ||| |||| | | ||| || | |||| ||| ||| | |||| || | ||| |  ║
╚══════════════════════════════════════════════════════════════════════╝
```

## ✈️&nbsp; Welcome aboard

### Francesco Wang &nbsp;·&nbsp; Senior DevOps Engineer @ [**AeroCloud**](https://aerocloudsystems.com)

[![Website](https://img.shields.io/badge/AeroCloud-aerocloudsystems.com-0A66C2?style=for-the-badge&logo=icloud&logoColor=white)](https://aerocloudsystems.com)

[![Operations](https://img.shields.io/badge/AOS-Airport_Operations-1f6feb?style=for-the-badge&logo=airbnb&logoColor=white)](https://aerocloudsystems.com/airport-operations-system/)

[![Processing](https://img.shields.io/badge/PAX-Passenger_Processing-2ea44f?style=for-the-badge&logo=airplay&logoColor=white)](https://aerocloudsystems.com/passenger-processing/)

[![Monitoring](https://img.shields.io/badge/PFM-Passenger_Flow-d4751d?style=for-the-badge&logo=googleanalytics&logoColor=white)](https://aerocloudsystems.com/passenger-flow-monitoring/)

</div>

---

## 🛫 &nbsp;Pre-flight Briefing

> Good morning, ladies and gentlemen. The weather over `main` is clear, the
> pipelines are green, and the runway is free. We are number one for takeoff.

I act as a multidisciplinary Platform Engineer with the versatility to operate across the full platform lifecycle. I move fluidly between the roles of Infrastructure Platform Engineer (IPE), Developer Experience Platform Engineer (DPE), Security Platform Engineer (SPE), and Observability Platform Engineer (OPE), using each perspective to bridge the gap between scalable infrastructure and seamless developer enablement.

## Things I Care About

```diff
+ Boring infrastructure. The best kind is the kind you don't notice.
+ Pipelines that fail fast and explain themselves.
+ Observability before features. You can't fix what you can't see.
+ Cost is a feature. So is sleep.
- Hero culture. If a deploy depends on one person being awake, it's broken.
- Manual runbooks. If it's a checklist, it's a script in waiting.
- "It works on my laptop." That laptop has never paid a customer.
```

---

## The Fleet - what AeroCloud builds

A cloud-native operations platform for airports. Three products, one mission:
**make the airport experience smoother for everyone**.

<table>
  <tr>
    <td width="33%" align="center" valign="top">
      <h3>🗼 Airport Operations System</h3>
      <p>
        AeroCloud Airport Operating Systems gives your team a single, real-time view of operations so you can act faster, plan smarter, and keep everything running smoothly.
      </p>
      <a href="https://aerocloudsystems.com/airport-operations-system/">
        <img src="https://img.shields.io/badge/Learn_more-→-1f6feb?style=flat-square" alt="AOS">
      </a>
    </td>
    <td width="33%" align="center" valign="top">
      <h3>🛂 Passenger Processing</h3>
      <p>
        AeroCloud’s CUPPS airport solutions are a cloud-native, common-use passenger processing system designed to help airports, FBOs, ground handlers, and airlines move passengers smoothly from arrival to boarding.
      </p>
      <a href="https://aerocloudsystems.com/passenger-processing/">
        <img src="https://img.shields.io/badge/Learn_more-→-2ea44f?style=flat-square" alt="PAX">
      </a>
    </td>
    <td width="33%" align="center" valign="top">
      <h3>📡 Passenger Flow Monitoring</h3>
      <p>
        AeroCloud’s Passenger Flow Monitoring System gives airports real-time visibility into queues, wait times, footfall patterns, and passenger movement. Teams can respond faster, plan smarter and make passenger experiences smoother throughout the terminal.
      </p>
      <a href="https://aerocloudsystems.com/passenger-flow-monitoring/">
        <img src="https://img.shields.io/badge/Learn_more-→-d4751d?style=flat-square" alt="PFM">
      </a>
    </td>
  </tr>
</table>

---

## Live Flight Radar

<!-- FLIGHT-DATA:START -->
```
╔══════════════════════════════════════════════════════════════════════╗
║       ✈   L I V E   G L O B A L   F L I G H T   R A D A R   ✈        ║
║                         2026-07-01 14:42 UTC                         ║
╠══════════════════════════════════════════════════════════════════════╣
║ Aircraft tracked worldwide .................................. 13,281 ║
║   └── currently airborne .................................... 12,267 ║
║   └── on the ground (taxi / parked) .......................... 1,014 ║
║                                                                      ║
║ Average cruise altitude .................................. 20,206 ft ║
║ Average ground speed ....................................... 310 kts ║
║ Highest flight (N53AA) ................................... 84,800 ft ║
║ Fastest flight (THY7CB) .................................. 2,625 kts ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 🌍  Busiest Skies Right Now

> Top countries by aircraft currently airborne.

| # | Country of registration | Aircraft aloft |
|:---:|:---|---:|
| 1 | United States | 6,798 |
| 2 | United Kingdom | 577 |
| 3 | Canada | 385 |
| 4 | Germany | 344 |
| 5 | Turkey | 337 |
| 6 | Ireland | 280 |
| 7 | France | 232 |
| 8 | China | 213 |

### 🛫  Today's Featured Hub — `DFW` · Dallas/Fort Worth

> _Bigger than the island of Manhattan - five parallel runways._

> Hubs at this scale are exactly where AeroCloud's **Airport Operations System** and **Passenger Flow Monitoring** earn their keep — every flight here is a small symphony of stands, gates, baggage belts, immigration desks, and people.

<sub>📡 Last transmission: <b>2026-07-01 14:42 UTC</b> &nbsp;·&nbsp; Source: <a href="https://opensky-network.org">OpenSky Network</a> (free, no API key) &nbsp;·&nbsp; Refreshed every 3 h by GitHub Actions.</sub>
<!-- FLIGHT-DATA:END -->

<details>
<summary>🛰️&nbsp; How does this work? (engineering notes)</summary>

<br>

A single script driven by one GitHub Actions workflow:

| Workflow | Trigger | Job |
|---|---|---|
| [`radar.yaml`](./.github/workflows/radar.yaml) | `cron: "0 */3 * * *"` | refresh README, commit if changed |

**How it works**

[`scripts/update_flights.py`](./scripts/update_flights.py) does everything in one pass: fetch → summarise → render → patch. It calls OpenSky's free `/states/all` endpoint, computes headline stats (aircraft counts, average altitude/speed, highest and fastest flights, top countries by airborne aircraft), renders a markdown block, and rewrites the section between the `FLIGHT-DATA` markers in this README. Stdlib only — no dependencies.

**Failure mode.** If OpenSky times out or returns junk, the script logs the cause, exits 0, and leaves the previous snapshot in place — a transient upstream blip never breaks the README.

**Footprint.** Single API call. ~1 second per sweep on a GitHub-hosted runner. No servers, no secrets, no cost.

</details>

---

## Approach & Landing - Get in Touch

<div align="center">

[![Contact Us](https://img.shields.io/badge/Contact-US-0A66C2?style=for-the-badge&logo=globe&logoColor=white)](https://aerocloudsystems.com/get-in-touch/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Page-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/aerocloud-systems/)

</div>

---

<div align="center">

```sh
__|__
--@--@--(_)--@--@--
✈  safe flight  ✈
```

<sub>This README runs on caffeine ☕ and refreshes its flight data every 3 hours via GitHub Actions.<br>
Live aircraft positions courtesy of the brilliant volunteers at the <a href="https://opensky-network.org">OpenSky Network</a>.</sub>

</div>
