"""Streamlit app for the Data Quality Monitor demo.

Wraps data_quality_checks.run_checks() and exposes it as a drag-drop CSV experience.
All copy is embedded so a cold visitor can read, understand, and try the demo
without leaving the page.
"""

from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from data_quality_checks import Finding, run_checks

ROOT = Path(__file__).parent
SAMPLE_CSV = ROOT / "sample_dataset.csv"

st.set_page_config(
    page_title="Data Quality Monitor — Isaac Maya",
    page_icon="📊",
    layout="wide",
)

# ---------- Hero ----------
st.title("📊 Data Quality Monitor")
st.markdown(
    "**Drop in any CSV. Get a six-dimension data quality verdict in 3 seconds.**  \n"
    "_Built to demonstrate: Data Quality Engineer · Analytics Engineer · QA Lead_"
)

# ---------- Why this exists ----------
with st.expander("📖 Why this exists", expanded=True):
    st.markdown(
        """
Most data-quality tooling is either enterprise-grade (Monte Carlo, Great Expectations) or
5-line `pandas` asserts. **Nothing in the middle.** This monitor proves you can ship a useful
DQ check in a weekend — and frame the findings so a business owner can act, not just an engineer.

Six dimensions are checked: **Completeness, Uniqueness, Validity, Anomaly, Lineage, Timeliness.**
Each finding ships with a recommended remediation in plain English. The status verdict at the top
tells you whether the data is safe to publish or needs review *before* you put it in front of an
executive.

Bring your own CSV. The sample is just there so you don't have to.
"""
    )

with st.expander("🎯 What you're looking at"):
    st.markdown(
        """
- ✅ Six DQ dimensions checked in parallel — Completeness, Uniqueness, Validity, Anomaly, Lineage, Timeliness
- ✅ Findings written in business language, not engineer-speak
- ✅ Severity-based release verdict — *publish-safe* vs *review-required*
- ✅ Median-based anomaly detection — no hardcoded thresholds
- ✅ Bring-your-own-CSV — no sample dataset lock-in
- ✅ Runs locally in your browser; no data leaves the Streamlit container
"""
    )

# ---------- Try it ----------
st.divider()
st.header("🧪 Try it")
st.info("👈 Upload your own CSV, or use the bundled sample. Required columns: `record_id`, `customer_id`, `transaction_date`, `region`, `order_amount`, `source_system`.")

uploaded = st.file_uploader("Drop a CSV here", type=["csv"], accept_multiple_files=False)

if uploaded is not None:
    df = pd.read_csv(uploaded)
    source_label = f"your upload: `{uploaded.name}`"
else:
    df = pd.read_csv(SAMPLE_CSV)
    source_label = "the bundled sample (`sample_dataset.csv`)"

st.caption(f"Currently scanning {source_label} — **{len(df)} rows**.")

rows = df.to_dict("records")
rows = [{k: ("" if pd.isna(v) else str(v)) for k, v in row.items()} for row in rows]
findings: list[Finding] = run_checks(rows)

high = sum(1 for f in findings if f.severity == "High")
medium = sum(1 for f in findings if f.severity == "Medium")
impacted = len({f.record_id for f in findings})

# ---------- Verdict banner ----------
if high == 0 and medium == 0:
    st.success(f"✅ **SAFE TO PUBLISH** — no issues found across {len(df)} rows.")
elif high == 0:
    st.warning(f"⚠️ **REVIEW BEFORE PUBLISHING** — {medium} medium-severity finding(s), 0 high.")
else:
    st.error(f"🛑 **DO NOT PUBLISH** — {high} high-severity finding(s) across {impacted} record(s). Resolve before reporting.")

# ---------- Top metrics + donut ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rows scanned", len(df))
col2.metric("Total findings", len(findings))
col3.metric("High severity", high)
col4.metric("Impacted records", impacted)

if findings:
    findings_df = pd.DataFrame([
        {"Dimension": f.check, "Severity": f.severity, "Record": f.record_id,
         "Field": f.field, "Issue": f.issue, "Recommended action": f.action}
        for f in findings
    ])

    # Donut by dimension
    dim_counts = findings_df.groupby(["Dimension", "Severity"]).size().reset_index(name="Count")
    fig = px.sunburst(
        dim_counts,
        path=["Dimension", "Severity"],
        values="Count",
        color="Severity",
        color_discrete_map={"High": "#d62728", "Medium": "#ff7f0e"},
        title="Findings by dimension and severity",
    )
    fig.update_layout(height=400, margin=dict(t=40, l=0, r=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

    # Filters
    col_sev, col_dim = st.columns(2)
    sev_filter = col_sev.multiselect(
        "Filter by severity", options=sorted(findings_df["Severity"].unique()),
        default=sorted(findings_df["Severity"].unique()),
    )
    dim_filter = col_dim.multiselect(
        "Filter by dimension", options=sorted(findings_df["Dimension"].unique()),
        default=sorted(findings_df["Dimension"].unique()),
    )
    filtered = findings_df[findings_df["Severity"].isin(sev_filter) & findings_df["Dimension"].isin(dim_filter)]

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    # Per-record drill-down
    if not filtered.empty:
        record_options = sorted(filtered["Record"].unique())
        chosen = st.selectbox(
            "Inspect a specific record — see the original row with the violating field highlighted",
            options=["(pick one)"] + list(record_options),
        )
        if chosen != "(pick one)":
            original = df[df["record_id"].astype(str) == chosen]
            if not original.empty:
                st.write(f"**Original row for `{chosen}`:**")
                st.dataframe(original, use_container_width=True, hide_index=True)
                violating_fields = sorted(filtered[filtered["Record"] == chosen]["Field"].unique())
                st.warning(f"Violating field(s): {', '.join('`' + f + '`' for f in violating_fields)}")
            else:
                st.info(f"Record `{chosen}` not in the source dataframe (may have been the missing-key finding).")
else:
    st.success("No findings — your data passed all six checks.")

# ---------- How to test it ----------
st.divider()
with st.expander("🧪 How to test it (guided tour)", expanded=True):
    st.markdown(
        """
**Step 1 — Read the verdict.** Load the bundled sample. You should see a 🛑 **DO NOT PUBLISH** banner. Note
which dimension wedge in the donut is largest — that's where the trouble lives.

**Step 2 — Filter to the high-severity issues.** Uncheck "Medium" in the severity filter. Read one
"Recommended action" cell — that's the deliverable a data lead would forward to the source-system owner.
Notice it's written in business language, not SQL.

**Step 3 — Drill into a record.** Pick a `record_id` from the dropdown. The original row appears with the
violating field(s) called out. This is the trace a data steward would attach to a remediation ticket.

**Step 4 — Break it on purpose.** Upload a clean CSV (no duplicate IDs, all amounts positive, no blanks) —
the verdict should flip to ✅ **SAFE TO PUBLISH**. Then upload one with a duplicate `record_id` value — watch
the verdict cross the high-severity threshold in real time.

**Step 5 — Try your own data.** The required columns are listed above. Most operational/transactional CSVs
fit the shape. The point isn't that this scanner replaces your DQ tooling — it's that the six dimensions
are a universal frame you can apply to any dataset.
"""
    )

with st.expander("💼 What this proves about me"):
    st.markdown(
        """
**For Data Quality Engineer roles:** I treat DQ as a release decision, not a metric. The verdict banner
*decides*, the donut *summarizes*, and the findings table *explains*. That order matters.

**For Analytics Engineer roles:** I write remediation in the voice of the person who has to do the fix.
"Confirm correction vs duplicate" is a deliverable. "Duplicate key detected" is an alarm.

**For QA Lead roles:** I make threshold logic visible — anomaly detection is `median × 8`, not a magic number.
A scanner you can argue with is a scanner you can trust.

---

**Isaac Maya** — QA · Agentic AI · Data Quality  \n
📧 theisaacmaya@icloud.com · 💼 [LinkedIn](https://linkedin.com/in/isaac-maya) · 🔗 [Source](https://github.com/isaac-maya/data-quality-monitor) · 📝 [Essays](https://isaac-maya.github.io/essays/)
"""
    )
