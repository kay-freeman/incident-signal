# Changelog

All notable changes to Incident Signal are documented in this file.

## [1.0.0] - 2026-08-01

### Added

- JSON support-ticket ingestion
- Required-field and data-type validation
- ISO timestamp validation
- Duplicate ticket-ID detection
- Configurable incident thresholds
- Configurable detection windows
- Category-based ticket grouping
- Chronological ticket processing
- Sliding-window incident detection
- Multiple-incident detection within the same category
- False-positive prevention for slow ticket activity
- Explainable `medium`, `high`, and `critical` severity scoring
- Human-readable text reports
- Structured JSON reports
- Configurable input-file selection
- Optional text and JSON report saving
- Automatic creation of missing report directories
- Clear input, configuration, and output errors
- Synthetic demonstration dataset
- Automated detection, ingestion, and reporting tests
- GitHub Actions continuous integration
- System requirements and acceptance-criteria documentation
- Architecture and design-decision documentation

### Verification

- 18 automated tests passing
- GitHub Actions passing on the `main` branch
- Sample dataset detects two separate login incidents
- Morning sample incident classified as `high`
- Afternoon sample incident classified as `medium`
- Unrelated sample tickets ignored
- Text and JSON reports verified
- Saved report output verified

### Privacy

- No customer data
- No employer data
- No credentials
- No proprietary ticket records
- Synthetic demonstration data only