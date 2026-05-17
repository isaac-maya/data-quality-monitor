# Data Quality Report

Run date: 2026-05-16

## Sendable Summary

This sample shows how a lightweight monitor can surface reporting risk and translate it into next actions a business or analytics owner can understand. The point is not a large rules engine; it is whether the output makes trust issues visible early.

## Executive Summary

Status: Needs review before executive or client-facing reporting.

- Rows scanned: 25
- Findings: 7 (4 high, 3 medium)
- Impacted records: 6

## Business Readout

The monitor found issues that could distort totals, trend commentary, or trust in source-system lineage. The priority actions are to resolve duplicate keys, blank customer IDs, non-positive amounts, and the high-value outlier before reporting.

## Findings

| Severity | Check | Record | Field | Issue | Recommended action |
| --- | --- | --- | --- | --- | --- |
| High | Validity | 1004 | order_amount | Amount is 0.00. | Exclude from totals until transaction state is resolved. |
| Medium | Anomaly | 1009 | order_amount | Amount 100,000.00 exceeds median-based threshold. | Validate with business owner before using in trend commentary. |
| High | Validity | 1011 | order_amount | Amount is -45.00. | Exclude from totals until transaction state is resolved. |
| High | Completeness | 1019 | customer_id | Required value is blank. | Enrich from source before publishing. |
| Medium | Lineage | 1020 | source_system | Unexpected source 'legacy'. | Confirm source approval and ownership. |
| Medium | Timeliness | 1024 | transaction_date | Date 2026-05-25 is after run date. | Check date parsing, timezone, or accidental future entry. |
| High | Uniqueness | 1024 | record_id | Duplicate primary key found. | Confirm correction vs duplicate and deduplicate. |

## Controls Demonstrated

- Completeness checks for required reporting fields.
- Duplicate key detection for auditability.
- Amount validity checks for credible totals.
- Median-based anomaly detection for review queues.
- Source-system allowlist for lineage confidence.
- Future-date guardrail for timeliness.
