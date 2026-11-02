# Froker Creator Acquisition Funnel Analysis

SQL + Python analysis that traces every creator through 4 activation stages, computes drop-off rates and cohort retention, and delivers one prioritised fix recommendation per major drop-off point.

> Built Aug 2024 – Aug 2025 — pure Python + SQL (SQLite). No BI tool required; findings are reproducible and version-controlled.

---

## Problem

The startup was spending budget acquiring creators (social ads, referrals, partnerships) but activation was poor. Marketing measured signups. Product measured posts. Nobody had connected the two to find where creators were dying in the funnel — so nobody was fixing the right thing.

---

## Funnel Stages

```
Stage 1: App signup
Stage 2: Profile complete (bio + niche + photo)
Stage 3: First post published
Stage 4: First brand deal accepted
```

---

## Key Finding (from demo data)

```
Stage 1 — Signup:          200  (100%)
Stage 2 — Profile Done:    156  (78.0%)   drop: 22.0%
Stage 3 — First Post:       64  (32.0%)   drop: 59.0%  ← WORST DROP
Stage 4 — First Deal:       39  (19.5%)   drop: 39.1%
```

**59% of creators who complete their profile never post.**

Root cause hypothesis: Creators sign up with intent but have no idea what to post first. There is no challenge suggestion, template, or prompt after profile completion. They open the app once after completing profile, see a blank "post" screen with no guidance, and never return.

**Recommended fix:** Day 3 push notification — *"Your first challenge is waiting — post a review of your favourite local spot and earn your first points."*
Expected impact: +15–20pp Stage 2→3 conversion.

---

## Cohort Retention Output

```
Month       Size    D7%    D14%    D30%
2024-09      104   18.3%   24.0%   28.8%
2024-10       96   17.7%   24.0%   29.2%
```

---

## Files

| File | Description |
|---|---|
| `funnel_analysis.py` | Full funnel + cohort analysis, finding + fix recommendation |
| `requirements.txt` | Dependencies |

---

## Run locally

```bash
pip install -r requirements.txt
python funnel_analysis.py
```

---

## Design Decisions

| Decision | Reasoning |
|---|---|
| Personal baseline per stage | Absolute conversion rates mean nothing without a "fix" — every drop-off comes with a hypothesis and a recommendation |
| Cohort by acquisition month | Seasonal effects matter. A creator acquired in October behaves differently than one acquired in a growth-sprint month |
| SQLite, no warehouse dependency | Reproducible analysis that any engineer can run locally. No access credentials required for portfolio demonstration |
