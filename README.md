# TruthGuard-AI
# TruthGuard Website — single-user test package

This is a separate website code package based on the locally supplied TruthGuard V3 website and the Project 1.1.0 app updates. It has not been deployed to an existing live site. No personal database, private backups, APK signing keys or passwords are included.

**Important: this is NOT a public or multi-customer production service.** It has one shared local SQLite workspace, not separate user accounts or customer isolation. The local token (if configured) is not a complete login system. Run only on your own computer, bound to 127.0.0.1. Do not expose it to the internet, a shared server, or customers without a proper reviewed authentication, per-user authorization, privacy controls, HTTPS, secure backups and deployment design. The `--demo-preview` flag explicitly permits a shared preview for disposable synthetic data only; never use it for private data.

## Run locally

Python 3.10+ is required (tested here on 3.13). Extract the ZIP, open this folder in a terminal, and run:

    python -m pip install -r requirements.txt
    python run.py

Open http://127.0.0.1:8000/ and keep the terminal open. On Windows you may double-click START_WINDOWS.bat after installing Python. DOCX import requires the dependency; the core runs on standard Python. At first launch a new database is created under `data/` with clearly marked demo records, hidden by default. Your previous app, website data and phone data are not automatically copied. This package intentionally starts with a new workspace.

## Changes and limits

- Updated app-style mobile/desktop interface, detector, reports, question-aware monitoring, npm monitoring and explicit structured INR product selection are carried over from Project 1.1.0. Developer menu and SQLite/cost status are hidden; this is not security.
- Scheduled checks run only while the server process is running; sleep, internet loss, a server restart and source-site changes can delay or stop checks. Review latest results and failures. The detector is conservative and does not automatically verify arbitrary claims or prove local product stock.
- Backup & Settings can download an unencrypted, private ZIP containing a checked SQLite snapshot. Keep it outside the computer in a safe place. The website currently **cannot import a downloaded ZIP**; it can restore snapshots already created on its own server. In an isolated synthetic test, this backup format was restored into the compatible Project app backend; restore replaces its workspace. Always back up first.
- Do not delete or overwrite an existing database to upgrade. Migration of actual personal or production data has not been verified. Old Android and web data are separate.
- There is no customer account setup or production deployment here. Before public use, build and test per-user isolation and permissions, select hosting, enable proper HTTPS, establish monitoring/restart and secure backup/restore, and perform a security review. Do not rely on the demo preview for private information.

## Tests

Automated browser checks at 320, 390 and 1280 px covered verification, menu, monitoring disclosure, backup ZIP data/integrity, reset warning and layout. Additional isolated checks covered product comparisons, supported source processing, conservative evidence semantics, portable backup core and URL security. A configured-token test checked the backup route; a local run rejects network binding unless explicitly started in demo preview mode. These are automated tests, not a production security review, deployment verification or real-device test.
