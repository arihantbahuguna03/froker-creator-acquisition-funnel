"""
Creator Acquisition Funnel Config — Example
============================================
Copy this file to funnel_config.py and fill in your calibrated values.
funnel_config.py is gitignored — this example shows the structure only.

Stage conversion rates were derived from real creator activation data.
These numbers reveal actual funnel performance and are not included
in this demo repo.
"""

# ── Stage conversion rates (probability of reaching each stage) ───────────────
# Calibrated from real acquisition data — not included in this demo repo.
STAGE_CONVERSION_RATES = {
    "profile_complete": None,   # % of signups who complete their profile
    "first_post":       None,   # % of profile-completers who post — typically the biggest drop
    "first_deal":       None,   # % of posters who accept a brand deal
}
