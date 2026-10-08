<!-- Hero banner: switches with the viewer's GitHub theme. Regenerate with `python3 scripts/build_banner.py`. -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./light.svg">
  <img alt="Ameya Ajit Kabir — Automation Developer & RPA Engineer" src="./dark.svg" width="100%">
</picture>

<p align="center">
  <a href="mailto:ameyakabir@gmail.com"><img src="https://img.shields.io/badge/ameyakabir@gmail.com-0F172A?style=flat-square&logo=gmail&logoColor=22D3EE" alt="Email"></a>
  <img src="https://img.shields.io/badge/Pune,%20India-0F172A?style=flat-square&logo=googlemaps&logoColor=10B981" alt="Pune, India">
  <img src="https://img.shields.io/badge/@%20AutomationEdge-0F172A?style=flat-square&logo=probot&logoColor=A78BFA" alt="AutomationEdge">
  <img src="https://komarev.com/ghpvc/?username=ameya-kabir&label=profile%20views&color=0F172A&style=flat-square" alt="Profile views">
</p>

<br>

## `> about`

```yaml
name:      Ameya Ajit Kabir
role:      Automation Developer · RPA Engineer
based:     Pune, India
building:  tools that run unattended — and tell you when something breaks
```

I build **automation that holds up in production**: enterprise web automation, API integrations and the database layers underneath them.

- **Enterprise IT alerting** — watchdog services with multi-level escalation, so incidents reach the right person before users notice.
- **Healthcare workflows** — RPA pipelines that move data between portals, APIs and databases without manual re-entry.
- **Developer tooling** — custom Chrome extensions for DOM inspection that make selector-hunting for web bots fast and repeatable.
- **Data architecture** — PostgreSQL schemas designed for auditability, reporting and the edge cases automation always finds.

<br>

## `> stack`

<div align="center">

| | |
|:--|:--|
| **Languages** | <img src="https://img.shields.io/badge/Java-0F172A?style=for-the-badge&logo=openjdk&logoColor=22D3EE" alt="Java"> <img src="https://img.shields.io/badge/Python-0F172A?style=for-the-badge&logo=python&logoColor=22D3EE" alt="Python"> <img src="https://img.shields.io/badge/JavaScript-0F172A?style=for-the-badge&logo=javascript&logoColor=22D3EE" alt="JavaScript"> <img src="https://img.shields.io/badge/SQL-0F172A?style=for-the-badge&logo=databricks&logoColor=22D3EE" alt="SQL"> <img src="https://img.shields.io/badge/HTML5-0F172A?style=for-the-badge&logo=html5&logoColor=22D3EE" alt="HTML5"> <img src="https://img.shields.io/badge/CSS3-0F172A?style=for-the-badge&logo=css3&logoColor=22D3EE" alt="CSS3"> |
| **Automation** | <img src="https://img.shields.io/badge/AutomationEdge-0F172A?style=for-the-badge&logo=data:image%2Fsvg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iIzM0RDM5OSIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMTEgMmgydjNoNWEyIDIgMCAwIDEgMiAydjEwYTIgMiAwIDAgMS0yIDJINmEyIDIgMCAwIDEtMi0yVjdhMiAyIDAgMCAxIDItMmg1VjJ6TTggMTBhMS41IDEuNSAwIDEgMCAwIDMgMS41IDEuNSAwIDAgMCAwLTN6bTggMGExLjUgMS41IDAgMSAwIDAgMyAxLjUgMS41IDAgMCAwIDAtM3pNOCAxNXYxLjVoOFYxNUg4ek0xIDloMnY2SDF6TTIxIDloMnY2aC0yeiIvPjwvc3ZnPg%3D%3D" alt="AutomationEdge"> <img src="https://img.shields.io/badge/Selenium-0F172A?style=for-the-badge&logo=selenium&logoColor=34D399" alt="Selenium"> <img src="https://img.shields.io/badge/REST%20APIs-0F172A?style=for-the-badge&logo=postman&logoColor=34D399" alt="REST APIs"> <img src="https://img.shields.io/badge/Chrome%20Extensions-0F172A?style=for-the-badge&logo=googlechrome&logoColor=34D399" alt="Chrome Extensions"> |
| **Data** | <img src="https://img.shields.io/badge/PostgreSQL-0F172A?style=for-the-badge&logo=postgresql&logoColor=A78BFA" alt="PostgreSQL"> <img src="https://img.shields.io/badge/MySQL-0F172A?style=for-the-badge&logo=mysql&logoColor=A78BFA" alt="MySQL"> <img src="https://img.shields.io/badge/MongoDB-0F172A?style=for-the-badge&logo=mongodb&logoColor=A78BFA" alt="MongoDB"> <img src="https://img.shields.io/badge/pandas-0F172A?style=for-the-badge&logo=pandas&logoColor=A78BFA" alt="pandas"> |
| **Web & Tooling** | <img src="https://img.shields.io/badge/Node.js-0F172A?style=for-the-badge&logo=nodedotjs&logoColor=E2E8F0" alt="Node.js"> <img src="https://img.shields.io/badge/Express-0F172A?style=for-the-badge&logo=express&logoColor=E2E8F0" alt="Express"> <img src="https://img.shields.io/badge/React-0F172A?style=for-the-badge&logo=react&logoColor=E2E8F0" alt="React"> <img src="https://img.shields.io/badge/Git-0F172A?style=for-the-badge&logo=git&logoColor=E2E8F0" alt="Git"> <img src="https://img.shields.io/badge/Linux-0F172A?style=for-the-badge&logo=linux&logoColor=E2E8F0" alt="Linux"> |

</div>

<br>

## `> featured builds`

| Project | What it does | Under the hood | Stack |
|:--|:--|:--|:--|
| 🛰️ **Enterprise IT Alerting System** | Always-on watchdog that monitors services and scheduled jobs, raises incidents the moment something fails, and walks them up a **multi-level escalation chain** until someone acknowledges. | Watchdog loop · escalation tiers with timeouts · incident state persisted for audit & reporting | `Java` `Python` `PostgreSQL` `AutomationEdge` |
| 🗼 **The Tower — BlueStacks HUD Overlay** | Automation overlay for *The Tower* running in BlueStacks: a heads-up display layered over the emulator that reads game state and drives repetitive actions hands-free. | Transparent always-on-top HUD · screen-state detection · scripted input to the emulator | `Python` `BlueStacks` |
| 💸 **Personal Expense Tracker** | Full-stack tracker for logging spending, categorising transactions and seeing where the money actually goes month over month. | Normalised PostgreSQL schema · REST API · aggregate queries powering the dashboard | `PostgreSQL` `Node.js` `Express` `JavaScript` |

<br>

## `> stats`

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=ameya-kabir&show_icons=true&include_all_commits=true&count_private=true&hide_border=false&border_radius=16&bg_color=0F172A&border_color=1E293B&title_color=22D3EE&icon_color=7C3AED&text_color=CBD5E1&ring_color=10B981">
  <img height="170" alt="GitHub stats" src="https://github-readme-stats.vercel.app/api?username=ameya-kabir&show_icons=true&include_all_commits=true&count_private=true&hide_border=false&border_radius=16&bg_color=F8FAFC&border_color=E2E8F0&title_color=2563EB&icon_color=06B6D4&text_color=334155&ring_color=10B981">
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=ameya-kabir&layout=compact&langs_count=8&hide_border=false&border_radius=16&bg_color=0F172A&border_color=1E293B&title_color=22D3EE&text_color=CBD5E1">
  <img height="170" alt="Top languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username=ameya-kabir&layout=compact&langs_count=8&hide_border=false&border_radius=16&bg_color=F8FAFC&border_color=E2E8F0&title_color=2563EB&text_color=334155">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com?user=ameya-kabir&background=0F172A&border=1E293B&border_radius=16&stroke=1E293B&ring=7C3AED&fire=22D3EE&currStreakNum=E2E8F0&sideNums=E2E8F0&currStreakLabel=22D3EE&sideLabels=94A3B8&dates=64748B">
  <img width="100%" alt="GitHub streak" src="https://streak-stats.demolab.com?user=ameya-kabir&background=F8FAFC&border=E2E8F0&border_radius=16&stroke=E2E8F0&ring=2563EB&fire=06B6D4&currStreakNum=0F172A&sideNums=0F172A&currStreakLabel=2563EB&sideLabels=475569&dates=64748B">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=ameya-kabir&bg_color=0F172A&color=94A3B8&title_color=22D3EE&line=22D3EE&point=7C3AED&area=true&area_color=7C3AED&hide_border=false&border_color=1E293B&radius=16&custom_title=Commit%20activity">
  <img width="100%" alt="Commit activity graph" src="https://github-readme-activity-graph.vercel.app/graph?username=ameya-kabir&bg_color=F8FAFC&color=475569&title_color=2563EB&line=06B6D4&point=2563EB&area=true&area_color=06B6D4&hide_border=false&border_color=E2E8F0&radius=16&custom_title=Commit%20activity">
</picture>

</div>

<br>

<p align="center">
  <sub><code>$ echo "if it's repetitive, it's a bug"</code> &nbsp;·&nbsp; open to automation, integration &amp; data-heavy problems</sub>
</p>
