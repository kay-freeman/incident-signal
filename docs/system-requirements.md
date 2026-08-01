# Incident Signal — System Requirements

## Document Information

| Field | Value |
|---|---|
| System | Incident Signal |
| Version | 1.0 |
| Status | Implemented |
| Document date | August 1, 2026 |
| Repository | `kay-freeman/incident-signal` |

## 1. Purpose

Incident Signal is a configurable support-operations system that analyzes timestamped support tickets and identifies clusters that may represent emerging service incidents.

The system is designed to help support and operations teams recognize related customer reports earlier, distinguish separate periods of incident activity, prioritize incidents using explainable severity levels, and produce reports that can be reviewed by people or consumed by other systems.

## 2. Business Problem

Support teams often receive the first indication of a service issue through individual customer tickets.

When tickets are investigated independently:

- Related reports may not be recognized as a shared incident.
- Escalation may be delayed.
- Support volume can increase before operations teams understand the scope.
- Separate incidents involving the same issue can be combined incorrectly.
- Manual incident summaries may be inconsistent.
- Downstream teams may not receive structured information.

Incident Signal addresses this problem by applying consistent detection, validation, classification, and reporting rules to ticket data.

## 3. Objectives

Incident Signal must:

1. Detect meaningful clusters of related support tickets.
2. Avoid flagging slow or unrelated ticket activity as an incident.
3. Distinguish separate incidents within the same category.
4. Prevent tickets from being counted in more than one incident.
5. Assign an explainable severity level to each incident.
6. Support configurable detection rules.
7. Validate incoming data before processing it.
8. Produce human-readable and machine-readable reports.
9. Save reports for operational handoff or downstream processing.
10. Automatically verify system behavior after code changes.

## 4. Stakeholders

| Stakeholder | Need |
|---|---|
| Support agents | Earlier awareness that individual reports may be related |
| Support team leads | Consistent criteria for recognizing and escalating incidents |
| Incident managers | Structured incident summaries with timing, volume, and severity |
| Engineering teams | Clear ticket evidence associated with a suspected incident |
| Systems analysts | Configurable rules, documented requirements, and traceable behavior |
| Integration developers | Stable JSON output for downstream automation |

## 5. Scope

### 5.1 In Scope for Version 1.0

- JSON ticket-file ingestion
- Required-field validation
- Data-type and blank-value validation
- ISO timestamp validation
- Duplicate ticket-ID detection
- Category-based ticket grouping
- Configurable ticket threshold
- Configurable time window
- Multiple-incident detection
- False-positive prevention
- Volume-based severity scoring
- Human-readable text reports
- Structured JSON reports
- Optional report-file saving
- Automated tests
- Continuous integration through GitHub Actions
- Synthetic demonstration data

### 5.2 Out of Scope for Version 1.0

- Live help-desk API connections
- Webhook ingestion
- CSV ingestion
- Persistent database storage
- User authentication
- Web dashboard
- Slack or Jira notifications
- Machine-learning classification
- Automatic incident resolution
- Production hosting

These capabilities may be considered for future versions but are not required for version 1.0 completion.

## 6. Assumptions and Constraints

### Assumptions

- Each ticket belongs to one issue category.
- Ticket timestamps represent the time each report was created.
- Categories have already been assigned before detection begins.
- Ticket IDs are expected to be unique.
- ISO-formatted timestamps are sufficient for the version 1.0 dataset.
- A quiet period longer than the configured window separates incident activity.
- Ticket volume is an acceptable initial indicator of severity.

### Constraints

- Version 1.0 processes local JSON files.
- Detection is performed in memory.
- Severity does not account for customer tier, revenue impact, geography, or affected product criticality.
- The system does not modify the source ticket file.
- Sample data must remain fictional and contain no proprietary information.
- Detection must remain deterministic and explainable.

## 7. Input Data Contract

The input file must contain a JSON list of ticket objects.

### Required Ticket Fields

| Field | Type | Required | Description | Example |
|---|---|---:|---|---|
| `ticket_id` | String | Yes | Unique ticket identifier | `TKT-1001` |
| `created_at` | String | Yes | ISO-formatted creation timestamp | `2026-07-26T09:02:00` |
| `category` | String | Yes | Normalized issue category | `login_failure` |
| `summary` | String | Yes | Short description of the reported issue | `User cannot sign in.` |

### Input Validation Rules

- The input file must exist.
- The file must contain valid JSON.
- The top-level JSON value must be a list.
- Every list item must be an object.
- Every ticket must contain all required fields.
- Required values must be non-empty strings.
- `created_at` must contain a valid ISO timestamp.
- `ticket_id` values must be unique.
- Invalid input must stop processing and return a clear error.

## 8. Business Rules

### BR-001: Category Grouping

Tickets must only be evaluated for incident activity alongside tickets with the same category.

### BR-002: Chronological Processing

Tickets within each category must be processed in chronological order regardless of their original input order.

### BR-003: Default Detection Rule

The default incident threshold is three same-category tickets within 30 minutes.

### BR-004: Configurable Detection Rule

Users may change the ticket threshold and time window without modifying source code.

### BR-005: Activity Separation

A gap longer than the configured time window starts a new activity cluster within the same category.

### BR-006: Cluster Qualification

An activity cluster only becomes an incident if it contains at least the configured number of tickets within the configured time window.

### BR-007: No Double-Counting

A ticket may belong to only one activity cluster and one detected incident.

### BR-008: Multiple Incidents

More than one activity cluster within the same category may qualify as a separate incident.

### BR-009: Severity Assignment

Severity must be calculated from ticket volume relative to the configured threshold.

| Rule | Severity |
|---|---|
| Ticket count is at least 1× but less than 2× the threshold | `medium` |
| Ticket count is at least 2× but less than 3× the threshold | `high` |
| Ticket count is at least 3× the threshold | `critical` |

### BR-010: Incident Ordering

Detected incidents must be returned in chronological order by their first ticket timestamp.

## 9. Functional Requirements

| ID | Requirement |
|---|---|
| FR-001 | The system shall accept a JSON ticket file through the `--input` option. |
| FR-002 | The system shall use the included synthetic ticket file when no input path is provided. |
| FR-003 | The system shall validate all input data before incident detection. |
| FR-004 | The system shall group tickets by category. |
| FR-005 | The system shall sort same-category tickets chronologically. |
| FR-006 | The system shall accept a configurable positive ticket threshold. |
| FR-007 | The system shall accept a configurable positive time window in minutes. |
| FR-008 | The system shall detect qualifying ticket clusters. |
| FR-009 | The system shall detect multiple incidents within the same category. |
| FR-010 | The system shall prevent tickets from being counted in multiple incidents. |
| FR-011 | The system shall reject activity that does not meet the threshold within the configured window. |
| FR-012 | The system shall assign `medium`, `high`, or `critical` severity to every incident. |
| FR-013 | The system shall produce a human-readable text report. |
| FR-014 | The system shall produce a structured JSON report. |
| FR-015 | The system shall include source, detection rule, summary, category, severity, ticket count, timestamps, and ticket IDs in JSON output. |
| FR-016 | The system shall optionally save a report through the `--output` option. |
| FR-017 | The system shall create missing parent directories when saving a report. |
| FR-018 | The system shall return a concise confirmation after saving a report. |
| FR-019 | The system shall return clear errors for invalid input or output operations. |
| FR-020 | The system shall provide command-line help for all supported options. |

## 10. Nonfunctional Requirements

| ID | Requirement |
|---|---|
| NFR-001 | Detection results must be deterministic for the same input and configuration. |
| NFR-002 | Detection and severity rules must be explainable without machine-learning interpretation. |
| NFR-003 | Ingestion, detection, reporting, and command-line responsibilities must remain separated. |
| NFR-004 | The system must not modify the source ticket file. |
| NFR-005 | Saved reports must use UTF-8 encoding. |
| NFR-006 | The repository must not contain customer data, employer data, credentials, or proprietary records. |
| NFR-007 | Automated tests must cover positive, negative, validation, reporting, and persistence behavior. |
| NFR-008 | GitHub Actions must run the complete test suite on every push and pull request. |
| NFR-009 | Version 1.0 must run using documented setup commands. |
| NFR-010 | Public documentation must match implemented behavior. |

## 11. Error Requirements

| Condition | Expected Result |
|---|---|
| Input file does not exist | Stop and report the missing path |
| JSON is malformed | Stop and report the line and column |
| Top-level data is not a list | Stop and report the required structure |
| Ticket is not an object | Stop and report its position |
| Required field is missing | Stop and identify the ticket position and field |
| Required value is blank or invalid | Stop and identify the affected field |
| Timestamp is invalid | Stop and identify the ticket and timestamp |
| Ticket ID is duplicated | Stop and identify the duplicate ID |
| Threshold is below one | Stop and reject the threshold |
| Window is below one minute | Stop and reject the window |
| Output format is unsupported | Reject the command and list supported formats |
| Report cannot be written | Stop and identify the selected output path |

## 12. Acceptance Criteria

Version 1.0 is accepted when all of the following are true:

- [x] Valid synthetic ticket data can be loaded successfully.
- [x] Invalid and incomplete ticket data is rejected.
- [x] The default threshold detects a qualifying incident.
- [x] Activity below the threshold is ignored.
- [x] Slow activity without a qualifying window is ignored.
- [x] Separate incidents in the same category are detected independently.
- [x] Tickets are not counted in multiple incidents.
- [x] Medium, high, and critical severity levels are assigned correctly.
- [x] Detection settings are configurable through command-line options.
- [x] Users can select an alternative JSON input file.
- [x] Reports can be displayed as text.
- [x] Reports can be displayed as JSON.
- [x] Text and JSON reports can be saved to files.
- [x] Missing report directories are created automatically.
- [x] Operational failures return clear errors.
- [x] Automated tests verify the implemented requirements.
- [x] GitHub Actions runs the tests on every push and pull request.
- [x] Public documentation contains no proprietary data.
- [x] The public README accurately explains the system.

## 13. Requirements Traceability

| Requirement area | Implementation | Verification |
|---|---|---|
| Data model | `src/models.py` | Detection and reporting tests |
| Input validation | `src/ingestion.py` | `tests/test_ingestion.py` |
| Detection rules | `src/detection.py` | `tests/test_detection.py` |
| Multiple incidents | `src/detection.py` | `test_detects_multiple_incidents_in_same_category` |
| False-positive prevention | `src/detection.py` | `test_activity_cluster_still_requires_qualifying_window` |
| Severity scoring | `src/detection.py` | `test_assigns_volume_based_severity` |
| Text reporting | `src/reporting.py` | `test_builds_readable_text_report` |
| JSON reporting | `src/reporting.py` | `test_builds_structured_json_report` |
| Report persistence | `src/reporting.py` | `test_saves_report_and_creates_parent_directory` |
| Command-line interface | `src/main.py` | Manual command validation |
| Continuous integration | `.github/workflows/tests.yml` | GitHub Actions workflow results |
| User documentation | `README.md` | Manual documentation review |

## 14. Success Measures

Incident Signal version 1.0 is considered successful when:

- All documented acceptance criteria are satisfied.
- All 18 automated tests pass locally.
- The GitHub Actions workflow passes on the `main` branch.
- The sample dataset produces two separate incidents.
- The morning sample incident is classified as `high`.
- The afternoon sample incident is classified as `medium`.
- The unrelated sample tickets are ignored.
- Text and JSON reports can be displayed and saved.
- A reviewer can understand the problem, rules, architecture, and results without reading every source file.