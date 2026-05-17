# Data Quality Monitor

🌐 **Live demo:** _coming soon — deploys to Hugging Face Spaces in Wave 2 rollout_

This compact artifact shows how I approach trustworthy analytics pipelines: define clear checks, surface anomalies, and translate findings into business-readable action.

## Contents

- `app.py`: Streamlit app — drag-drop any CSV, get a six-dimension data quality verdict in 3 seconds.
- `data_quality_checks.py`: local checker with six rules (Completeness, Uniqueness, Validity, Anomaly, Lineage, Timeliness).
- `sample_dataset.csv`: synthetic operational records with realistic defects.
- `quality_report.md`: generated stakeholder report from the CLI runner.
- `requirements.txt`: Streamlit + pandas + plotly.

## Run

**Interactive (Streamlit):**
```bash
pip install -r requirements.txt
streamlit run app.py
```

**CLI report:**
```bash
python3 data_quality_checks.py
```

## What It Demonstrates In 30 Seconds

- Simple rules can still produce useful anomaly and remediation output.
- The report is written for stakeholders, not only for engineers.
- The value is in trust and usability, not in pretending six checks are a full governance program.

## Company Hooks

| Target | Hook |
| --- | --- |
| Compass Group Canada | Operational reporting trust, anomaly visibility, and business-readable remediation. |
| BDO Data Quality | Rule design, exception evidence, lineage checks, and audit-friendly action language. |
| CGI data roles | Data validation, governance-minded delivery, client-readable reporting, and pipeline reliability. |
| EA analytics support | Dashboard readiness, anomaly triage, and quality gates for decision-making data. |

## Outreach Hook

I built a small data-quality monitor that surfaces anomalies and translates them into business-readable actions. I wanted the artifact to show trust and usability, not just rule-writing.
