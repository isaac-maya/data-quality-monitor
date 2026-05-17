"""Compact data-quality checks with business-readable report output."""

from __future__ import annotations

import csv
import statistics
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


DATASET_PATH = Path(__file__).with_name("sample_dataset.csv")
REPORT_PATH = Path(__file__).with_name("quality_report.md")
RUN_DATE = date.today()


@dataclass(frozen=True)
class Finding:
    check: str
    severity: str
    record_id: str
    field: str
    issue: str
    action: str


def load_rows(path: Path = DATASET_PATH) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def amount(row: dict[str, str]) -> float:
    try:
        return float(row.get("order_amount", "0"))
    except ValueError:
        return 0.0


def parse_day(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def run_checks(rows: list[dict[str, str]]) -> list[Finding]:
    findings: list[Finding] = []
    required = ("record_id", "customer_id", "transaction_date", "region", "order_amount")
    seen_ids: set[str] = set()
    positive_amounts = [amount(row) for row in rows if amount(row) > 0]
    outlier_threshold = statistics.median(positive_amounts) * 8

    for row in rows:
        record_id = row.get("record_id", "<missing>")
        for field in required:
            if not row.get(field, "").strip():
                findings.append(Finding("Completeness", "High", record_id, field, "Required value is blank.", "Enrich from source before publishing."))

        if record_id in seen_ids:
            findings.append(Finding("Uniqueness", "High", record_id, "record_id", "Duplicate primary key found.", "Confirm correction vs duplicate and deduplicate."))
        seen_ids.add(record_id)

        row_amount = amount(row)
        if row_amount <= 0:
            findings.append(Finding("Validity", "High", record_id, "order_amount", f"Amount is {row_amount:.2f}.", "Exclude from totals until transaction state is resolved."))
        if row_amount > outlier_threshold:
            findings.append(Finding("Anomaly", "Medium", record_id, "order_amount", f"Amount {row_amount:,.2f} exceeds median-based threshold.", "Validate with business owner before using in trend commentary."))

        if row.get("source_system") not in {"crm", "erp"}:
            findings.append(Finding("Lineage", "Medium", record_id, "source_system", f"Unexpected source '{row.get('source_system')}'.", "Confirm source approval and ownership."))

        transaction_date = parse_day(row.get("transaction_date", ""))
        if transaction_date and transaction_date > RUN_DATE:
            findings.append(Finding("Timeliness", "Medium", record_id, "transaction_date", f"Date {transaction_date.isoformat()} is after run date.", "Check date parsing, timezone, or accidental future entry."))

    return findings


def render_report(rows: list[dict[str, str]], findings: list[Finding]) -> str:
    high = sum(1 for item in findings if item.severity == "High")
    medium = sum(1 for item in findings if item.severity == "Medium")
    impacted = len({item.record_id for item in findings})
    lines = [
        "# Data Quality Report",
        "",
        f"Run date: {RUN_DATE.isoformat()}",
        "",
        "## Sendable Summary",
        "",
        "This sample shows how a lightweight monitor can surface reporting risk and translate it into next actions a business or analytics owner can understand. The point is not a large rules engine; it is whether the output makes trust issues visible early.",
        "",
        "## Executive Summary",
        "",
        "Status: Needs review before executive or client-facing reporting.",
        "",
        f"- Rows scanned: {len(rows)}",
        f"- Findings: {len(findings)} ({high} high, {medium} medium)",
        f"- Impacted records: {impacted}",
        "",
        "## Business Readout",
        "",
        "The monitor found issues that could distort totals, trend commentary, or trust in source-system lineage. The priority actions are to resolve duplicate keys, blank customer IDs, non-positive amounts, and the high-value outlier before reporting.",
        "",
        "## Findings",
        "",
        "| Severity | Check | Record | Field | Issue | Recommended action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in findings:
        lines.append(f"| {item.severity} | {item.check} | {item.record_id} | {item.field} | {item.issue} | {item.action} |")
    lines.extend([
        "",
        "## Controls Demonstrated",
        "",
        "- Completeness checks for required reporting fields.",
        "- Duplicate key detection for auditability.",
        "- Amount validity checks for credible totals.",
        "- Median-based anomaly detection for review queues.",
        "- Source-system allowlist for lineage confidence.",
        "- Future-date guardrail for timeliness.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    rows = load_rows()
    findings = run_checks(rows)
    REPORT_PATH.write_text(render_report(rows, findings), encoding="utf-8")
    print(f"Scanned {len(rows)} rows; found {len(findings)} findings.")


if __name__ == "__main__":
    main()
