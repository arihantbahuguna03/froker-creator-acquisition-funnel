"""
Froker Creator Acquisition Funnel Analysis
==========================================
Traces every creator through 4 activation stages and computes
drop-off rates, cohort retention, and a prioritised fix recommendation.

Built Aug 2024 – Aug 2025 — pure Python + SQL (SQLite demo).

Problem:
  Froker is acquiring creators but activation is low. Marketing sees
  signup numbers, product sees post numbers — nobody has connected the
  two to find where creators are dying in the funnel.

Funnel stages:
  1. App download / signup
  2. Profile complete (bio + niche + photo)
  3. First post published
  4. First brand deal accepted

Output:
  - Stage-by-stage conversion rates
  - Cohort retention at Day 7, Day 14, Day 30
  - One finding + one fix recommendation per major drop-off
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

# ── Demo dataset ─────────────────────────────────────────────────────────────

DEMO_CREATORS = []
base = datetime(2024, 9, 1)

import random
random.seed(42)

for i in range(200):
    signup = base + timedelta(days=random.randint(0, 60))

    # Stage 2: 78% complete profile
    profile_complete = signup + timedelta(days=random.randint(0, 2)) if random.random() < 0.78 else None

    # Stage 3: only 41% of profile-completers post (big drop)
    first_post = None
    if profile_complete and random.random() < 0.41:
        first_post = profile_complete + timedelta(days=random.randint(1, 14))

    # Stage 4: 62% of posters get a brand deal
    first_deal = None
    if first_post and random.random() < 0.62:
        first_deal = first_post + timedelta(days=random.randint(3, 30))

    DEMO_CREATORS.append({
        "creator_id":        f"DEMO_CREATOR_{i+1:03d}",
        "signup_date":       signup,
        "profile_complete":  profile_complete,
        "first_post_date":   first_post,
        "first_deal_date":   first_deal,
        "acquisition_month": signup.strftime("%Y-%m"),
    })


# ── SQLite setup ──────────────────────────────────────────────────────────────

def setup_db(conn: sqlite3.Connection) -> None:
    conn.execute("DROP TABLE IF EXISTS creators")
    conn.execute("""
        CREATE TABLE creators (
            creator_id        TEXT PRIMARY KEY,
            signup_date       TEXT,
            profile_complete  TEXT,
            first_post_date   TEXT,
            first_deal_date   TEXT,
            acquisition_month TEXT
        )
    """)
    conn.executemany(
        "INSERT INTO creators VALUES (?,?,?,?,?,?)",
        [
            (
                c["creator_id"],
                c["signup_date"].date().isoformat() if c["signup_date"] else None,
                c["profile_complete"].date().isoformat() if c["profile_complete"] else None,
                c["first_post_date"].date().isoformat() if c["first_post_date"] else None,
                c["first_deal_date"].date().isoformat() if c["first_deal_date"] else None,
                c["acquisition_month"],
            )
            for c in DEMO_CREATORS
        ],
    )
    conn.commit()


# ── Funnel analysis ───────────────────────────────────────────────────────────

FUNNEL_SQL = """
SELECT
    COUNT(*)                                              AS stage1_signup,
    SUM(CASE WHEN profile_complete IS NOT NULL THEN 1 ELSE 0 END)  AS stage2_profile,
    SUM(CASE WHEN first_post_date  IS NOT NULL THEN 1 ELSE 0 END)  AS stage3_first_post,
    SUM(CASE WHEN first_deal_date  IS NOT NULL THEN 1 ELSE 0 END)  AS stage4_first_deal
FROM creators
"""

COHORT_SQL = """
SELECT
    acquisition_month,
    COUNT(*)                                                        AS cohort_size,
    SUM(CASE WHEN first_post_date IS NOT NULL
         AND julianday(first_post_date) - julianday(signup_date) <= 7  THEN 1 ELSE 0 END) AS active_day7,
    SUM(CASE WHEN first_post_date IS NOT NULL
         AND julianday(first_post_date) - julianday(signup_date) <= 14 THEN 1 ELSE 0 END) AS active_day14,
    SUM(CASE WHEN first_post_date IS NOT NULL
         AND julianday(first_post_date) - julianday(signup_date) <= 30 THEN 1 ELSE 0 END) AS active_day30
FROM creators
GROUP BY acquisition_month
ORDER BY acquisition_month
"""


def run_funnel(conn: sqlite3.Connection) -> None:
    row = conn.execute(FUNNEL_SQL).fetchone()
    s1, s2, s3, s4 = row

    print("\n" + "="*65)
    print("  FROKER CREATOR ACQUISITION FUNNEL")
    print("="*65)
    print(f"\n  Stage 1 — Signup:         {s1:>4}  (100%)")
    print(f"  Stage 2 — Profile Done:   {s2:>4}  ({s2/s1*100:.1f}%)  drop: {(1-s2/s1)*100:.1f}%")
    print(f"  Stage 3 — First Post:     {s3:>4}  ({s3/s1*100:.1f}%)  drop: {(1-s3/s2)*100:.1f}% from S2")
    print(f"  Stage 4 — First Deal:     {s4:>4}  ({s4/s1*100:.1f}%)  drop: {(1-s4/s3)*100:.1f}% from S3")

    print("\n\n  KEY FINDING:")
    worst_drop   = max([(1-s2/s1, 2), (1-s3/s2, 3), (1-s4/s3, 4)], key=lambda x: x[0])
    stage_labels = {2: "Profile → First Post", 3: "Profile Done → First Post", 4: "First Post → First Deal"}
    print(f"  ⚠️  Biggest drop is at Stage {worst_drop[1]}: {worst_drop[0]*100:.1f}% of creators lost")

    if worst_drop[1] == 3:
        print("\n  ROOT CAUSE HYPOTHESIS:")
        print("  Creators complete their profile but don't know what to post first.")
        print("  There is no prompt, template, or challenge suggestion after profile completion.\n")
        print("  RECOMMENDED FIX:")
        print("  Day 3 push notification: 'Your first challenge is waiting — post a review")
        print("  of your favourite local spot and earn your first points.'")
        print("  Expected impact: +15–20pp Stage 2→3 conversion based on industry benchmarks.\n")


def run_cohorts(conn: sqlite3.Connection) -> None:
    rows = conn.execute(COHORT_SQL).fetchall()

    print("\n" + "="*65)
    print("  COHORT RETENTION (Day 7 / Day 14 / Day 30 activation)")
    print("="*65)
    print(f"\n  {'Month':<12} {'Size':>6} {'D7%':>7} {'D14%':>7} {'D30%':>7}")
    print("  " + "-"*45)
    for r in rows:
        month, n, d7, d14, d30 = r
        print(f"  {month:<12} {n:>6} {d7/n*100:>6.1f}% {d14/n*100:>6.1f}% {d30/n*100:>6.1f}%")
    print()


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    setup_db(conn)
    run_funnel(conn)
    run_cohorts(conn)
    conn.close()
