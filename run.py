#!/usr/bin/env python3
"""TruthGuard AI — Version 3 local launcher.

Tagline: VERIFY ONCE. MONITOR CONTINUOUSLY.
Zero-cost, offline-capable local application with safe V1/V2->V3 SQLite migration
and active-process local monitoring scheduler.
"""

from __future__ import annotations

import argparse
from http.server import ThreadingHTTPServer
from pathlib import Path

from backend.api.handlers import ApiApplication, make_request_handler
from backend.config import (
    APP_NAME,
    APP_SUBTITLE,
    APP_TAGLINE,
    APP_VERSION,
    DEFAULT_DB_PATH,
    DEFAULT_HOST,
    DEFAULT_PORT,
)
from backend.database import DatabaseManager
from backend.seed_data import seed_database


def create_initialized_app(
    db_path: Path = DEFAULT_DB_PATH,
    *,
    start_scheduler: bool = False,
    auth_token: str | None = None,
    rate_limit_rpm: int | None = None,
) -> ApiApplication:
    db = DatabaseManager(db_path)
    db.init_schema()
    if db.is_empty():
        seed_database(db)
    kwargs = {"start_scheduler": start_scheduler}
    if auth_token is not None:
        kwargs["auth_token"] = auth_token
    if rate_limit_rpm is not None:
        kwargs["rate_limit_rpm"] = rate_limit_rpm
    return ApiApplication(db, **kwargs)


def main() -> None:
    parser = argparse.ArgumentParser(description=f"{APP_NAME} ({APP_VERSION}) Local Server")
    parser.add_argument("--host", default="127.0.0.1", help="Local interface (default: 127.0.0.1)")
    parser.add_argument("--demo-preview", action="store_true", help="Allow network binding for synthetic demonstration data only; not production secure")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="TCP port to listen on (default: 8000)")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="Path to local SQLite database file")
    parser.add_argument("--no-scheduler", action="store_true", help="Disable local active-process background scheduler")
    args = parser.parse_args()

    if args.host not in ("127.0.0.1", "localhost", "::1") and not args.demo_preview:
        parser.error("Network exposure is disabled. This single-user app has no customer isolation. Use loopback only.")
    if args.demo_preview:
        print("WARNING: Demo preview is not private. Use synthetic data only.", flush=True)

    # Match the Project APK: all fetched external source URLs and redirects require HTTPS.
    from urllib.parse import urlsplit
    import backend.services.security_service as security
    original_validate_url = security.validate_public_http_url
    def validate_https_url(url, *args, **kwargs):
        if not isinstance(url, str) or urlsplit(url.strip()).scheme.lower() != "https":
            raise security.SecurityValidationError("External source fetching requires HTTPS, including redirects.")
        return original_validate_url(url, *args, **kwargs)
    security.validate_public_http_url = validate_https_url

    app = create_initialized_app(
        Path(args.db),
        start_scheduler=not args.no_scheduler,
    )
    handler_cls = make_request_handler(app)
    server = ThreadingHTTPServer((args.host, args.port), handler_cls)

    print("=" * 72)
    print(f"  {APP_NAME} — {APP_VERSION}")
    print(f"  {APP_SUBTITLE}")
    print(f"  {APP_TAGLINE}")
    print("-" * 72)
    print(f"  Mode       : V3 Local (Explainable Verification Engine)")
    print(f"  Database   : {Path(args.db).resolve()}")
    print(f"  Scheduler  : {'Active (local process only)' if app.monitoring_service.scheduler_running else 'Disabled'}")
    print(f"  Listening  : http://{args.host}:{args.port}")
    print(f"  API Docs   : http://{args.host}:{args.port}/api/v3/docs")
    print("=" * 72)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[TruthGuard] Shutting down local server and scheduler cleanly...")
    finally:
        app.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
